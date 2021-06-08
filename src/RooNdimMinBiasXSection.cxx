#include "RooNdimMinBiasXSection.h"
#include <string>  
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "Common.h"
using namespace std;

RooNdimMinBiasXSection::RooNdimMinBiasXSection(const char* name , const char* title ,
					       MultiBinMaker* mbm , XSectionWeight* xsw , RooArgList& variables): RooAbsPdf( name, title ),
														  MBM(mbm),
														  XSW(xsw),
														  xsecProxy("xsection" , "xsection" , this , *(XSW->xsection) ),
														  f1DProjected(false){
  for(int i=0 ; i< variables.getSize() ;i++){
    allProxyVars.emplace( allProxyVars.end() , variables[i].GetName() , variables[i].GetName() ,
			  this , dynamic_cast<RooRealVar&>(variables[i]) ) ;
  }
};
RooNdimMinBiasXSection::RooNdimMinBiasXSection(const char* name , const char* title ,
					       MultiBinMaker* mbm , XSectionWeight* xsw, RooMultiDimCategory& one_d ): RooAbsPdf( name, title ),
														       MBM(mbm),
														       XSW(xsw),
														       xsecProxy("xsection" , "xsection" , this , *(XSW->xsection) ),
														       f1DProjected(true),
														       f1DVariable(one_d.GetName() , one_d.GetName() , this , one_d){
};
RooNdimMinBiasXSection::RooNdimMinBiasXSection(const RooNdimMinBiasXSection& other , const char* name): RooAbsPdf(other ,name),
													MBM(other.MBM),
													XSW(other.XSW),
													xsecProxy( "xsection" , this , other.xsecProxy ),
													f1DProjected(other.f1DProjected),
													f1DVariable(other.f1DVariable.GetName() , this , other.f1DVariable){
  for(auto vproxy : other.allProxyVars){
    allProxyVars.emplace( allProxyVars.end() , vproxy.GetName() , this , vproxy );
  }
  // if(f1DProjected){
  //   RooRealProxy tmp(other.f1DVariable.GetName() , this , other.f1DVariable);
  //   f1DVariable = tmp;
  // }
  cout << "Copy of RooNdimMinBiasXSection";
};

TObject* RooNdimMinBiasXSection::clone(const char* newname) const{
  return new RooNdimMinBiasXSection(*this , newname);
};

Double_t RooNdimMinBiasXSection::evaluate() const {
#ifdef DEBUGL
  if(DEBUGL > 5)

    cout << "pdf val for xsec:"<<(double)xsecProxy << " and " ;
#endif
  TH1* nIntractions;
  if(f1DProjected){
    int binId = (int)f1DVariable;
    nIntractions = MBM->getNInteractions(binId);
#ifdef DEBUGL
    if(DEBUGL > 5)

      cout << "binId:" << binId ;
#endif
  }else{
    double vals[ allProxyVars.size() ];
    for(long unsigned int ii=0 ; ii < allProxyVars.size() ; ii++){
      double v = (double)(allProxyVars[ii]);
      vals[ii] = v;
#ifdef DEBUGL
      if(DEBUGL > 5)

	cout << allProxyVars[ii].GetName() << ":" << v << ";" ;
      cout << allProxyVars[ii].GetName() << ":" << v <<  " and ";
#endif
    }
    // cout << endl;
    nIntractions = MBM->getNInteractions(vals);
  }
  TH1* weights = XSW->getWeights((double)xsecProxy);

  double ret11 = 0;
  for(int i =1 ; i < nIntractions->GetNbinsX()+1 ; i++){
    double bc = nIntractions->GetBinCenter(i);
    int bi = weights->FindBin( bc );
    double w = weights->GetBinContent(bi);
    double l = nIntractions->GetBinContent(bi);

    ret11 += w*l ;
  }

#ifdef DEBUGL
  if(DEBUGL > 5)
    cout << " is : " << ret11 << endl;
#endif
  return ret11;
};

ClassImp(RooNdimMinBiasXSection);

