#ifndef MULTIBINMAKER_h
#define MULTIBINMAKER_h

#include "TH1.h"
#include "TTree.h"
#include "TKDTreeBinning.h"
#include "RooArgList.h"
#include <string>  
#include <algorithm>
#include <stdexcept>
#include <sstream>
using namespace std;

class RooNdimMinBiasXSection;

class MultiBinMaker : public TObject {
  friend class RooNdimMinBiasXSection;
public:
  MultiBinMaker( TTree* t , RooArgList varNames , int NBINS , bool LoadHists = true );

  MultiBinMaker(const MultiBinMaker& other, const char* name=0);
  
  virtual TObject* clone(const char* name) const;
  inline virtual ~MultiBinMaker() {};

  // TH1* getNInteractions();
  TH1* getNInteractions(double* vals);
  TH1* getNInteractions(int binId);

  const double* GetBinCenter(unsigned int bin) const;

  const TKDTreeBinning* getKDBinning() const;
protected:
  TKDTreeBinning* fKdBinning;
  //RooArgList& variables;
  std::map<int , TH1*> fHNInts;

  void loadHists(TTree* t,RooArgList& variables);

  ClassDef(MultiBinMaker,1) 
private:
  template<class t>
  string joinStrings(vector<t> x ,const string delimiter) {
    stringstream  s;
    copy(x.begin(),x.end(), ostream_iterator<t>(s,delimiter.c_str()));
    auto ret = s.str();
    return ret.substr(0 , ret.size()-delimiter.size());
  };
};

#endif
