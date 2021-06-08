#ifndef ROONDIMMINBIASXSECTION_h
#define ROONDIMMINBIASXSECTION_h

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooRealVar.h"

#include "XSectionWeight.h"
#include "MultiBinMaker.h"
#include "RooMultiDimCategory.h"
using namespace std;

class RooNdimMinBiasXSection : public RooAbsPdf {
public:
  RooNdimMinBiasXSection() {};
  RooNdimMinBiasXSection(const char* name , const char* title ,
			 MultiBinMaker* mbm , XSectionWeight* xsw , RooArgList& variables);
  RooNdimMinBiasXSection(const char* name , const char* title ,
			 MultiBinMaker* mbm , XSectionWeight* xsw , RooMultiDimCategory& one_d );       
  RooNdimMinBiasXSection(const RooNdimMinBiasXSection& other , const char* name = 0);
  virtual TObject* clone(const char* newname) const override;
  inline virtual ~RooNdimMinBiasXSection() {} ;

protected:
  MultiBinMaker* MBM;
  XSectionWeight* XSW;
  bool f1DProjected;

  Double_t evaluate() const override;

  RooRealProxy xsecProxy;
  std::vector<RooRealProxy> allProxyVars;
  RooRealProxy f1DVariable;
private:
  
  ClassDefOverride(RooNdimMinBiasXSection,1)
};
  
#endif

