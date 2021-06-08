#ifndef ROO_MULTIBIN_CATEGORY
#define ROO_MULTIBIN_CATEGORY

#include "RooRealVar.h"
#include "RooAbsRealLValue.h"
#include "RooRealProxy.h"
#include "RooArgList.h"
#include "TKDTreeBinning.h"
#include <vector>
#include <utility>
  
//#include "RooFitLegacy/RooCatTypeLegacy.h"

using namespace std;

class RooMultiDimCategory : public RooAbsRealLValue {
  
public:
  // Constructors etc.
  RooMultiDimCategory():InputVars(*(new RooArgList())) {};
  RooMultiDimCategory(const char* name, const char *title,RooArgList& inputVars,
		      const TKDTreeBinning* kdBinning);
  RooMultiDimCategory(const RooMultiDimCategory& other, const char *name=0);
  virtual TObject* clone(const char* newname) const override;

  virtual void setVal(Double_t value) override;
  virtual std::list<std::string> getBinningNames() const override;
  virtual const RooAbsBinning& getBinning(const char* name=0, Bool_t verbose=kTRUE, Bool_t createOnTheFly=kFALSE) const override;
  virtual RooAbsBinning& getBinning(const char* name=0, Bool_t verbose=kTRUE, Bool_t createOnTheFly=kFALSE) override;
  virtual Bool_t hasBinning(const char* name) const override;
  
protected:
  const TKDTreeBinning* tkdBinning;
  vector<RooRealProxy> _inputVars ;
  RooArgList& InputVars;
  RooAbsBinning* theBinning;

  void addCategories();
  
  virtual value_type evaluate() const override;
  /// No shape recomputation is necessary. This category does not depend on other categories.
  //void recomputeShape() override;
  
  ClassDefOverride(RooMultiDimCategory, 1) // Real-to-Category function defined by series of thresholds
};
  
#endif

