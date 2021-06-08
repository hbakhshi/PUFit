#include "RooMultiDimCategory.h"
#include "RooUniformBinning.h"
#include "Common.h"

ClassImp(RooMultiDimCategory);


RooMultiDimCategory::RooMultiDimCategory(const char* name, const char *title,RooArgList& inputVars,
					 const TKDTreeBinning* kdBinning): RooAbsRealLValue(name , title),
									   tkdBinning( kdBinning ),
									   InputVars(inputVars){
  for(int i=0 ; i< inputVars.getSize() ;i++){
    _inputVars.emplace( _inputVars.end() , inputVars[i].GetName() , inputVars[i].GetName() ,
			this , dynamic_cast<RooRealVar&>(inputVars[i]) ) ;
  }
  addCategories();
};

RooMultiDimCategory::RooMultiDimCategory(const RooMultiDimCategory& other, const char *name):RooAbsRealLValue(other , name),
											     tkdBinning( other.tkdBinning),
											     InputVars(other.InputVars){
  for(auto vproxy : other._inputVars){
    _inputVars.emplace( _inputVars.end() , vproxy.GetName() , this , vproxy );
  }
  addCategories();
};

TObject* RooMultiDimCategory::clone(const char* newname) const { return new RooMultiDimCategory(*this, newname); };


void RooMultiDimCategory::addCategories() {
  unsigned int nbins = tkdBinning->GetNBins();
  theBinning = new RooUniformBinning(0 , nbins , nbins , "default");
};

RooMultiDimCategory::value_type RooMultiDimCategory::evaluate() const{
  double vals[ _inputVars.size() ];
  for(long unsigned int ii=0 ; ii < _inputVars.size() ; ii++){
    double v = (double)(_inputVars[ii]);
    //cout << _inputVars[ii].GetName() << ":" << v << ";" ;
    vals[ii] = v;
  }
  //cout << " -> " << tkdBinning->FindBin( vals ) << endl;
  return tkdBinning->FindBin( vals );
};

void RooMultiDimCategory::setVal(Double_t value){
#ifdef DEBUGL
  if(DEBUGL > 5)
    cout << "setVal to" << value << ",";
#endif
  if(value >= tkdBinning->GetNBins())
    value = tkdBinning->GetNBins()-1;

  unsigned int binId(value);
  const double* binCenters = tkdBinning->GetBinCenter(binId);
  for(int i=0 ; i< InputVars.getSize() ;i++){
    dynamic_cast<RooRealVar&>(InputVars[i]).setVal(binCenters[i]);
    _inputVars[i] = binCenters[i];
#ifdef DEBUGL
    if(DEBUGL > 5)
      cout << _inputVars[i].GetName() << "-" << (double)(_inputVars[i]) << "==" << binCenters[i] << ","<< dynamic_cast<RooRealVar&>(InputVars[i]).getVal() << ";" ;
#endif
  }
  // if(binId != evaluate() )
#ifdef DEBUGL
  if(DEBUGL > 5)
    cout << "setVal(" << value << "), evaluate()==" << evaluate() << endl;
#endif
};

std::list<std::string> RooMultiDimCategory::getBinningNames() const{
  std::list<std::string> ret;
  ret.push_back("default");
  return ret;
};
const RooAbsBinning& RooMultiDimCategory::getBinning(const char* name, Bool_t verbose, Bool_t createOnTheFly) const{
  return *theBinning;
};
RooAbsBinning& RooMultiDimCategory::getBinning(const char* name, Bool_t verbose, Bool_t createOnTheFly){
  return *theBinning;
};
Bool_t RooMultiDimCategory::hasBinning(const char* name) const{
  return name=="default";
};

/// No shape recomputation is necessary. This category does not depend on other categories.
//void RooMultiDimCategory::recomputeShape(){ }
