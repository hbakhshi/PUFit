#ifndef ROOMINBIASXSECTION_h
#define ROOMINBIASXSECTION_h

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TH2.h"
#include <algorithm>
#include <stdexcept>
#include <sstream>
using namespace std;

class RooMinBiasXSection : public RooAbsPdf {
public:
  RooMinBiasXSection() { };
  RooMinBiasXSection(const char *name, const char *title,
		     TH2* _h2d, RooAbsReal& _xsection , RooAbsReal& _x);
  
  RooMinBiasXSection(const RooMinBiasXSection& other, const char* name=0);
  virtual TObject* clone(const char* newname) const override;
  inline virtual ~RooMinBiasXSection() { };
    
protected:
  TH2* H2d;

  RooAbsReal* __x;
  RooAbsReal* __xsection;
  
  RooRealProxy fXSection;
  RooRealProxy fXVar;
  //std::vector<TH1*> allHistos;
  
  Double_t evaluate() const override;
  //RooSpan<double> evaluateSpan(RooBatchCompute::RunContext& evalData, const RooArgSet* normSet) const override;
  
private:
  
  ClassDefOverride(RooMinBiasXSection,1) // RooMinBiasXSection
};
  
#endif

