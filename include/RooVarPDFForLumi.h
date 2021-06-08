#ifndef ROOVARPDFFORLUMI_h
#define ROOVARPDFFORLUMI_h

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TH2.h"
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "RooRealVar.h"
using namespace std;

class RooVarPDFForLumi : public RooAbsPdf {
public:
  RooVarPDFForLumi() { };
  RooVarPDFForLumi(const char *name, const char *title,
		   TH2* _h2dSimulation, TH1* lumiDist,
		   RooAbsReal& _xsection , RooAbsReal& _x , double deltaT , TDirectory* dir=NULL);
  
  RooVarPDFForLumi(const RooVarPDFForLumi& other, const char* name=0);
  virtual TObject* clone(const char* newname) const override;
  inline virtual ~RooVarPDFForLumi() { };
    
protected:
  TH2* h2dSimulation;
  TH1* lumiDist;
  TH2* h2dVarVsXSec;
  double DeltaT;
  
  RooRealVar* __x;
  RooRealVar* __xsection;
  
  RooRealProxy fXSection;
  RooRealProxy fXVar;
  //std::vector<TH1*> allHistos;
  
  Double_t evaluate() const override;
  //RooSpan<double> evaluateSpan(RooBatchCompute::RunContext& evalData, const RooArgSet* normSet) const override;
  
private:
  void make2dHist(TDirectory* dir=NULL);
  
  ClassDefOverride(RooVarPDFForLumi,1) // RooVarPDFForLumi
};
  
#endif

