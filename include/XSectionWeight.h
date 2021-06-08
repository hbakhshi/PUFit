#ifndef XSECTIONWEIGHT_h
#define XSECTIONWEIGHT_h

#define NOMINALXSEC 69200

#include "RooAbsReal.h"
#include "TFile.h"
#include "TH1.h"
#include <algorithm>
#include <stdexcept>
#include <sstream>
using namespace std;

class RooNdimMinBiasXSection;

class XSectionWeight : public TObject {
  friend class RooNdimMinBiasXSection;
public:
  XSectionWeight() {};
  XSectionWeight( const char* fname , TH1* simnTrue , RooAbsReal* _xsection );
  XSectionWeight( const XSectionWeight& other, const char* name=0);

  virtual TObject* clone(const char* name) const;
  inline virtual ~XSectionWeight() {};

  TH1* getWeights();
  TH1* getWeights(double xsec);
protected:
  std::map< int , TH1* > nPuData;
  std::vector<int> availableXSecBins;
  TH1* simNTrue;
  RooAbsReal* xsection;

  ClassDefOverride(XSectionWeight,1) 
};
  
#endif

