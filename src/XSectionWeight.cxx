#include "XSectionWeight.h"
#include <string>  
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "Common.h"
using namespace std;

XSectionWeight::XSectionWeight( const char* fname , TH1* simnTrue , RooAbsReal* _xsection ):xsection(_xsection)
{
  simNTrue = (TH1*)(simnTrue->Clone());
  simNTrue->Scale( 1.0 / simNTrue->Integral() );
  simNTrue->SetDirectory(0);
    
  TFile* f = TFile::Open(fname);
  for(int i=830 ; i < 1171 ; i++){
    TObject* h1 = f->Get(TString("h_" + to_string(i)));
    if( !h1 ){
      cout << "ninteractions in data for pu " << i << " is not found" << endl;
      continue;
    }
    availableXSecBins.push_back( i );
    auto h = (TH1*)(h1->Clone());
    h->Scale( 1.0 / h->Integral() );
    h->SetDirectory(0);
    h->Divide( simNTrue );
    nPuData[i] = h;
  }
  f->Close();
};

XSectionWeight::XSectionWeight( const XSectionWeight& other, const char* name):TObject(other),
										 xsection(other.xsection ),
										 nPuData( other.nPuData),
										 simNTrue( other.simNTrue )
{
  cout << "Copy of XSectionWeight" << endl;
};

TObject* XSectionWeight::clone(const char* name) const{
  return new XSectionWeight(*this , name);
};


TH1* XSectionWeight::getWeights(){
  double xsec = xsection->getVal();
  return getWeights(xsec);
};

TH1* XSectionWeight::getWeights(double xsec){
  int binxsec = 1000+floor(1000*(xsec - NOMINALXSEC)/NOMINALXSEC);
  
  if( std::find(availableXSecBins.begin(), availableXSecBins.end(), binxsec) == availableXSecBins.end() ){
    auto const it = std::lower_bound(availableXSecBins.begin(), availableXSecBins.end(), binxsec);
    if (it == availableXSecBins.end()) { return NULL; }
    
    binxsec = *it;
  }
    
  auto hdata = nPuData[binxsec];
  //cout << "XSectionWeight:" << xsec << endl;
  return hdata;
};
ClassImp(XSectionWeight); 

