#include "MultiBinMaker.h"
#include <string>  
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "RooRealVar.h"
#include "TH1.h"
#include "Common.h"

using namespace std;

MultiBinMaker::MultiBinMaker( TTree* t , RooArgList varNames , int NBINS , bool LoadHists ){
  
  RooArgList& variables(varNames);

  if(varNames.getSize() > 4 ){
    throw range_error("up to 4 variables are supported by MultiBinMaker");
  }

  vector<TString> vNames;
  for(int ii=0 ;ii < varNames.getSize() ; ii++)
    vNames.push_back( varNames[ii].GetName() );
    
  TString formula = joinStrings(vNames , ":");
  cout << formula << endl;

  t->SetEstimate( t->GetEntries() );
  long long DATASZ = t->Draw( formula , "" , "goff" );
  int DATADIM = varNames.getSize() ;
  vector<double> smp; //[DATASZ * DATADIM];
    
  for (int i = 0; i < DATADIM; ++i){
    double* vals = t->GetVal(i);
    double min_ = *min_element(vals , vals+DATASZ) ;
    double max_ = *max_element(vals, vals+DATASZ);
    dynamic_cast<RooRealVar&>(varNames[i]).setRange(min_,max_);
      
    variables[i].Print();
    for (UInt_t j = 0; j < DATASZ; ++j){
      smp.push_back( vals[j] );
    }
  }
  fKdBinning = new TKDTreeBinning(DATASZ, DATADIM, smp, NBINS);
  if(DATADIM==1)
    fKdBinning->SortOneDimBinEdges(true);
  else 
    fKdBinning->SortBinsByDensity(true);
  if(LoadHists)
    loadHists(t , variables);
  smp.clear();
};

void MultiBinMaker::loadHists(TTree* t , RooArgList& variables){

  unsigned int nbins = fKdBinning->GetNBins();
  unsigned int dim   = fKdBinning->GetDim();
  const double* binsMinEdges = fKdBinning->GetBinsMinEdges();
  const double* binsMaxEdges = fKdBinning->GetBinsMaxEdges();
  for (unsigned int i = 0; i < nbins; ++i) {
    int edgeDim = i * dim;
    vector<TString> cuts ; 
    for(int k = 0 ; k < variables.getSize() ; k++){
      auto varN = TString(variables[k].GetName());
      auto MinEdge = binsMinEdges[edgeDim+k];
      auto MaxEdge = binsMaxEdges[edgeDim+k];

      cuts.push_back( "(" + varN + ">=" + TString(to_string(MinEdge)) + ")" );
      cuts.push_back( "(" + varN + " < " + TString(to_string(MaxEdge)) + ")" );
    }
    auto cutstr = joinStrings( cuts , "&&" );
    cout << "bin " << i << ":" << cutstr << flush;
    TH1* h = new TH1D( TString("hnIntBin" + to_string(i)) , TString("hnIntBin" + to_string(i)) , 100 , 0 , 100 );
    auto nEvents=t->Draw( TString( "nInt>>hnIntBin" + to_string(i) ) , cutstr.c_str() , "goff" );
    cout << ":" << nEvents << endl;
    fHNInts[i] = h;
  }
};

MultiBinMaker::MultiBinMaker(const MultiBinMaker& other, const char* name):TObject(other),
									   fHNInts( other.fHNInts ),
									   fKdBinning( other.fKdBinning ){
  cout << "Copy of MultiBinMaker" << endl;
};
  
TObject* MultiBinMaker::clone(const char* name) const{
  return new MultiBinMaker(*this , name);
};


// TH1* MultiBinMaker::getNInteractions(){
//   double vals[ variables.getSize() ];
//   for(int i=0 ; i< variables.getSize() ;i++)
//     vals[i] = dynamic_cast<RooRealVar&>(variables[i]).getVal();
//   return getNInteractions( vals );
// };

TH1* MultiBinMaker::getNInteractions(double* vals) {
  int binId = fKdBinning->FindBin( vals );
  // cout << "MBM," << binId << ":" ;
  // for(long unsigned int i=0 ; i<sizeof(vals)/sizeof(vals[0]); i++)
  //   cout << vals[i] << "," ;
  // cout << endl;
  return getNInteractions(binId);
};
TH1* MultiBinMaker::getNInteractions(int binId) {
  return fHNInts[binId];
};
const double* MultiBinMaker::GetBinCenter(unsigned int bin) const{
  if(bin >= fKdBinning->GetNBins())
    bin = fKdBinning->GetNBins()-1;
  return fKdBinning->GetBinCenter( bin );
};

const TKDTreeBinning* MultiBinMaker::getKDBinning() const{
  return fKdBinning;
};

ClassImp(MultiBinMaker); 

