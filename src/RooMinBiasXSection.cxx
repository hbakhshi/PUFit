#include "RooMinBiasXSection.h"
#include <string>  
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include "Common.h"

using namespace std;


RooMinBiasXSection::RooMinBiasXSection(const char *name, const char *title,
				       TH2* _h2d, RooAbsReal& _xsection , RooAbsReal& _x) : RooAbsPdf(name,title),
											    fXSection("xsection" , "XSection" , this , _xsection),
											    fXVar("x" , "X" , this , _x)
{
  H2d = _h2d;
  
    __x = &_x ;
    __xsection = &_xsection;
    //load histograms from directory and keep the relation with fXSection value
    //analyze one of the histograms and make the fXVar variable
};
  
RooMinBiasXSection::RooMinBiasXSection(const RooMinBiasXSection& other, const char* name): RooAbsPdf(other,name),
											     fXSection("xsection",this,other.fXSection),
											     fXVar("x", this , other.fXVar),
											     __x(other.__x),
											     __xsection(other.__xsection){
  H2d = other.H2d;
};
TObject* RooMinBiasXSection::clone(const char* newname) const {
  return new RooMinBiasXSection(*this,newname);
};
  
Double_t RooMinBiasXSection::evaluate() const {
  const double xsec = fXSection;
  const double xxx = fXVar;
  //std::cout << "evaluate is called" << xsec << "," << xxx << std::endl;
  return  H2d->GetBinContent(H2d->FindBin(xxx,fXSection));
};

ClassImp(RooMinBiasXSection);


