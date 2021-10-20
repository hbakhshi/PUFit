#include "RooVarPDFForLumi.h"
#include <string>  
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "TDirectory.h"
#include "Common.h"
#include "TMath.h"

using namespace std;


RooVarPDFForLumi::RooVarPDFForLumi(const char *name, const char *title,
				   TH2* _h2d, TH1* lumiDist_ ,
				   RooAbsReal& _xsection , RooAbsReal& _x , double deltaT , TDirectory* dir) : RooAbsPdf(name,title),
													       fXSection("xsection" , "XSection" , this , _xsection),
													       fXVar("x" , "X" , this , _x){
  h2dSimulation = _h2d;
  lumiDist = lumiDist_;
  lumiDist->Scale( 1.0 / lumiDist->Integral() );
  DeltaT = deltaT;

  if(dir){
    dir->cd();
    lumiDist->Write("normalizedLumi");
  }
  
  __x = dynamic_cast<RooRealVar*>(&_x) ;
  __xsection = dynamic_cast<RooRealVar*>(&_xsection);

  make2dHist(dir);
  //load histograms from directory and keep the relation with fXSection value
  //analyze one of the histograms and make the fXVar variable
};

RooVarPDFForLumi::RooVarPDFForLumi(const char *name, const char *title,
				   RooAbsReal& _xsection , RooAbsReal& _x , TH2* h2dVarVsXSec_) : RooAbsPdf(name,title),
												 fXSection("xsection" , "XSection" , this , _xsection),
												 fXVar("x" , "X" , this , _x){
  h2dSimulation = NULL;
  lumiDist = NULL;
  DeltaT = -1;
  
  __x = dynamic_cast<RooRealVar*>(&_x) ;
  __xsection = dynamic_cast<RooRealVar*>(&_xsection);

  h2dVarVsXSec = h2dVarVsXSec_;
};

void RooVarPDFForLumi::make2dHist(TDirectory* dir){
  double varBins[ __x->getBinning().numBoundaries() ] ;
  for(int ii=0; ii < __x->getBinning().numBoundaries()-1 ; ii++){
    varBins[ii] = __x->getBinning().binLow(ii);
    cout << varBins[ii] << ";" ;
  }
  varBins[ __x->getBinning().numBoundaries()-1 ] = __x->getBinning().binHigh(__x->getBinning().numBoundaries()-2);
  cout << varBins[ __x->getBinning().numBoundaries()-1 ] << endl;
  double xsecBins[ __xsection->getBinning().numBoundaries() ] ;
  for(int ii=0; ii < __xsection->getBinning().numBoundaries()-1 ; ii++)
    xsecBins[ii] = __xsection->getBinning().binLow(ii);
  xsecBins[ __xsection->getBinning().numBoundaries()-1 ] = __xsection->getBinning().binHigh(__xsection->getBinning().numBoundaries()-2);
  cout << xsecBins << endl;
  h2dVarVsXSec = new TH2D("h2dVarVsXSec_" + TString(this->GetName()) , "" , __xsection->getBinning().numBoundaries()-1 , xsecBins , __x->getBinning().numBoundaries()-1 , varBins );

  TDirectory* puHistDir = NULL;
  if(dir){
    puHistDir = dir->mkdir( "PUProfiles" );
  }
  TH1D hPUForXSec("hPUForXSec_tmp" , "" , h2dSimulation->GetNbinsY() , h2dSimulation->GetYaxis()->GetXmin() , h2dSimulation->GetYaxis()->GetXmax() );
  for(int ii=0; ii < __xsection->getBinning().numBoundaries()-1 ; ii++){
    double xsection = __xsection->getBinning().binCenter(ii);
    hPUForXSec.Reset();
    for(int i=0; i < lumiDist->GetNbinsX() ; i++){
      double lambda = xsection*lumiDist->GetXaxis()->GetBinCenter(i+1)*DeltaT;
      double lumiProb = lumiDist->GetBinContent(i+1);

      for(int j=0 ; j < hPUForXSec.GetNbinsX() ; j++){
	int pu(hPUForXSec.GetXaxis()->GetBinLowEdge(j+1)) ;
	double currentVal = hPUForXSec.GetBinContent(j+1);
	hPUForXSec.SetBinContent( j+1 , currentVal+lumiProb*(TMath::Poisson(pu , lambda)) ); //pu==int(lambda);
      }
    }
    if(puHistDir){
      puHistDir->cd();
      string name = "hPuForXSec_" + to_string(ii);
      hPUForXSec.SetTitle( to_string( xsection ).c_str() );
      hPUForXSec.Write(name.c_str());
    }
    
    for(int j=0 ; j < hPUForXSec.GetNbinsX() ; j++){
      int pu(hPUForXSec.GetXaxis()->GetBinLowEdge(j+1)) ;
      double currentVal = hPUForXSec.GetBinContent(j+1);

      TH1* hVarForPU = h2dSimulation->ProjectionX( "_px" , j+1 , j+2 );
      if(hVarForPU->Integral() == 0)
          continue;
      hVarForPU->Scale( 1.0 / hVarForPU->Integral() );
      for(int i = 0 ; i<hVarForPU->GetNbinsX() ; i++){
	double val = hVarForPU->GetBinCenter(i+1);
	int binId = h2dVarVsXSec->FindBin( xsection , val);
	h2dVarVsXSec->SetBinContent( binId , h2dVarVsXSec->GetBinContent(binId)+currentVal*hVarForPU->GetBinContent(i+1));
      }

      delete hVarForPU;
    }
    
  }
  if(dir){
    dir->cd();
    h2dVarVsXSec->Write();
  }
};

RooVarPDFForLumi::RooVarPDFForLumi(const RooVarPDFForLumi& other, const char* name): RooAbsPdf(other,name),
										     fXSection("xsection",this,other.fXSection),
										     fXVar("x", this , other.fXVar),
										     __x(other.__x),
										     __xsection(other.__xsection){
  h2dSimulation = other.h2dSimulation;
  lumiDist = other.lumiDist;
  DeltaT = other.DeltaT;
  
  h2dVarVsXSec = other.h2dVarVsXSec;
};
TObject* RooVarPDFForLumi::clone(const char* newname) const {
  return new RooVarPDFForLumi(*this,newname);
};
  
Double_t RooVarPDFForLumi::evaluate() const {
  const double xsec = fXSection;
  const double xxx = fXVar;
  //std::cout << "evaluate is called" << xsec << "," << xxx << std::endl;
  return  h2dVarVsXSec->GetBinContent(h2dVarVsXSec->FindBin(fXSection, xxx));
};

ClassImp(RooVarPDFForLumi);


