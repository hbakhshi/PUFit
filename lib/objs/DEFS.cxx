// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME dOdOdIlibdIobjsdIDEFS
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualifies STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "MultiBinMaker.h"
#include "RooMinBiasXSection.h"
#include "RooNdimMinBiasXSection.h"
#include "XSectionWeight.h"
#include "RooMultiDimCategory.h"
#include "RooVarPDFForLumi.h"

// Header files passed via #pragma extra_include

namespace ROOT {
   static void delete_MultiBinMaker(void *p);
   static void deleteArray_MultiBinMaker(void *p);
   static void destruct_MultiBinMaker(void *p);
   static void streamer_MultiBinMaker(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::MultiBinMaker*)
   {
      ::MultiBinMaker *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::MultiBinMaker >(0);
      static ::ROOT::TGenericClassInfo 
         instance("MultiBinMaker", ::MultiBinMaker::Class_Version(), "MultiBinMaker.h", 16,
                  typeid(::MultiBinMaker), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::MultiBinMaker::Dictionary, isa_proxy, 16,
                  sizeof(::MultiBinMaker) );
      instance.SetDelete(&delete_MultiBinMaker);
      instance.SetDeleteArray(&deleteArray_MultiBinMaker);
      instance.SetDestructor(&destruct_MultiBinMaker);
      instance.SetStreamerFunc(&streamer_MultiBinMaker);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::MultiBinMaker*)
   {
      return GenerateInitInstanceLocal((::MultiBinMaker*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::MultiBinMaker*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_RooMinBiasXSection(void *p = 0);
   static void *newArray_RooMinBiasXSection(Long_t size, void *p);
   static void delete_RooMinBiasXSection(void *p);
   static void deleteArray_RooMinBiasXSection(void *p);
   static void destruct_RooMinBiasXSection(void *p);
   static void streamer_RooMinBiasXSection(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooMinBiasXSection*)
   {
      ::RooMinBiasXSection *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RooMinBiasXSection >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RooMinBiasXSection", ::RooMinBiasXSection::Class_Version(), "RooMinBiasXSection.h", 13,
                  typeid(::RooMinBiasXSection), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::RooMinBiasXSection::Dictionary, isa_proxy, 16,
                  sizeof(::RooMinBiasXSection) );
      instance.SetNew(&new_RooMinBiasXSection);
      instance.SetNewArray(&newArray_RooMinBiasXSection);
      instance.SetDelete(&delete_RooMinBiasXSection);
      instance.SetDeleteArray(&deleteArray_RooMinBiasXSection);
      instance.SetDestructor(&destruct_RooMinBiasXSection);
      instance.SetStreamerFunc(&streamer_RooMinBiasXSection);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooMinBiasXSection*)
   {
      return GenerateInitInstanceLocal((::RooMinBiasXSection*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RooMinBiasXSection*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_XSectionWeight(void *p = 0);
   static void *newArray_XSectionWeight(Long_t size, void *p);
   static void delete_XSectionWeight(void *p);
   static void deleteArray_XSectionWeight(void *p);
   static void destruct_XSectionWeight(void *p);
   static void streamer_XSectionWeight(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::XSectionWeight*)
   {
      ::XSectionWeight *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::XSectionWeight >(0);
      static ::ROOT::TGenericClassInfo 
         instance("XSectionWeight", ::XSectionWeight::Class_Version(), "XSectionWeight.h", 16,
                  typeid(::XSectionWeight), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::XSectionWeight::Dictionary, isa_proxy, 16,
                  sizeof(::XSectionWeight) );
      instance.SetNew(&new_XSectionWeight);
      instance.SetNewArray(&newArray_XSectionWeight);
      instance.SetDelete(&delete_XSectionWeight);
      instance.SetDeleteArray(&deleteArray_XSectionWeight);
      instance.SetDestructor(&destruct_XSectionWeight);
      instance.SetStreamerFunc(&streamer_XSectionWeight);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::XSectionWeight*)
   {
      return GenerateInitInstanceLocal((::XSectionWeight*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::XSectionWeight*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_RooMultiDimCategory(void *p = 0);
   static void *newArray_RooMultiDimCategory(Long_t size, void *p);
   static void delete_RooMultiDimCategory(void *p);
   static void deleteArray_RooMultiDimCategory(void *p);
   static void destruct_RooMultiDimCategory(void *p);
   static void streamer_RooMultiDimCategory(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooMultiDimCategory*)
   {
      ::RooMultiDimCategory *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RooMultiDimCategory >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RooMultiDimCategory", ::RooMultiDimCategory::Class_Version(), "RooMultiDimCategory.h", 16,
                  typeid(::RooMultiDimCategory), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::RooMultiDimCategory::Dictionary, isa_proxy, 16,
                  sizeof(::RooMultiDimCategory) );
      instance.SetNew(&new_RooMultiDimCategory);
      instance.SetNewArray(&newArray_RooMultiDimCategory);
      instance.SetDelete(&delete_RooMultiDimCategory);
      instance.SetDeleteArray(&deleteArray_RooMultiDimCategory);
      instance.SetDestructor(&destruct_RooMultiDimCategory);
      instance.SetStreamerFunc(&streamer_RooMultiDimCategory);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooMultiDimCategory*)
   {
      return GenerateInitInstanceLocal((::RooMultiDimCategory*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RooMultiDimCategory*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_RooNdimMinBiasXSection(void *p = 0);
   static void *newArray_RooNdimMinBiasXSection(Long_t size, void *p);
   static void delete_RooNdimMinBiasXSection(void *p);
   static void deleteArray_RooNdimMinBiasXSection(void *p);
   static void destruct_RooNdimMinBiasXSection(void *p);
   static void streamer_RooNdimMinBiasXSection(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooNdimMinBiasXSection*)
   {
      ::RooNdimMinBiasXSection *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RooNdimMinBiasXSection >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RooNdimMinBiasXSection", ::RooNdimMinBiasXSection::Class_Version(), "RooNdimMinBiasXSection.h", 15,
                  typeid(::RooNdimMinBiasXSection), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::RooNdimMinBiasXSection::Dictionary, isa_proxy, 16,
                  sizeof(::RooNdimMinBiasXSection) );
      instance.SetNew(&new_RooNdimMinBiasXSection);
      instance.SetNewArray(&newArray_RooNdimMinBiasXSection);
      instance.SetDelete(&delete_RooNdimMinBiasXSection);
      instance.SetDeleteArray(&deleteArray_RooNdimMinBiasXSection);
      instance.SetDestructor(&destruct_RooNdimMinBiasXSection);
      instance.SetStreamerFunc(&streamer_RooNdimMinBiasXSection);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooNdimMinBiasXSection*)
   {
      return GenerateInitInstanceLocal((::RooNdimMinBiasXSection*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RooNdimMinBiasXSection*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_RooVarPDFForLumi(void *p = 0);
   static void *newArray_RooVarPDFForLumi(Long_t size, void *p);
   static void delete_RooVarPDFForLumi(void *p);
   static void deleteArray_RooVarPDFForLumi(void *p);
   static void destruct_RooVarPDFForLumi(void *p);
   static void streamer_RooVarPDFForLumi(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooVarPDFForLumi*)
   {
      ::RooVarPDFForLumi *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RooVarPDFForLumi >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RooVarPDFForLumi", ::RooVarPDFForLumi::Class_Version(), "RooVarPDFForLumi.h", 14,
                  typeid(::RooVarPDFForLumi), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &::RooVarPDFForLumi::Dictionary, isa_proxy, 16,
                  sizeof(::RooVarPDFForLumi) );
      instance.SetNew(&new_RooVarPDFForLumi);
      instance.SetNewArray(&newArray_RooVarPDFForLumi);
      instance.SetDelete(&delete_RooVarPDFForLumi);
      instance.SetDeleteArray(&deleteArray_RooVarPDFForLumi);
      instance.SetDestructor(&destruct_RooVarPDFForLumi);
      instance.SetStreamerFunc(&streamer_RooVarPDFForLumi);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooVarPDFForLumi*)
   {
      return GenerateInitInstanceLocal((::RooVarPDFForLumi*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const ::RooVarPDFForLumi*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));
} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr MultiBinMaker::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *MultiBinMaker::Class_Name()
{
   return "MultiBinMaker";
}

//______________________________________________________________________________
const char *MultiBinMaker::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MultiBinMaker*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int MultiBinMaker::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::MultiBinMaker*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *MultiBinMaker::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MultiBinMaker*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *MultiBinMaker::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::MultiBinMaker*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr RooMinBiasXSection::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RooMinBiasXSection::Class_Name()
{
   return "RooMinBiasXSection";
}

//______________________________________________________________________________
const char *RooMinBiasXSection::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooMinBiasXSection*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RooMinBiasXSection::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooMinBiasXSection*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RooMinBiasXSection::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooMinBiasXSection*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RooMinBiasXSection::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooMinBiasXSection*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr XSectionWeight::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *XSectionWeight::Class_Name()
{
   return "XSectionWeight";
}

//______________________________________________________________________________
const char *XSectionWeight::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::XSectionWeight*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int XSectionWeight::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::XSectionWeight*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *XSectionWeight::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::XSectionWeight*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *XSectionWeight::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::XSectionWeight*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr RooMultiDimCategory::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RooMultiDimCategory::Class_Name()
{
   return "RooMultiDimCategory";
}

//______________________________________________________________________________
const char *RooMultiDimCategory::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooMultiDimCategory*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RooMultiDimCategory::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooMultiDimCategory*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RooMultiDimCategory::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooMultiDimCategory*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RooMultiDimCategory::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooMultiDimCategory*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr RooNdimMinBiasXSection::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RooNdimMinBiasXSection::Class_Name()
{
   return "RooNdimMinBiasXSection";
}

//______________________________________________________________________________
const char *RooNdimMinBiasXSection::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooNdimMinBiasXSection*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RooNdimMinBiasXSection::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooNdimMinBiasXSection*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RooNdimMinBiasXSection::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooNdimMinBiasXSection*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RooNdimMinBiasXSection::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooNdimMinBiasXSection*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr RooVarPDFForLumi::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RooVarPDFForLumi::Class_Name()
{
   return "RooVarPDFForLumi";
}

//______________________________________________________________________________
const char *RooVarPDFForLumi::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooVarPDFForLumi*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RooVarPDFForLumi::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooVarPDFForLumi*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RooVarPDFForLumi::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooVarPDFForLumi*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RooVarPDFForLumi::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooVarPDFForLumi*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
void MultiBinMaker::Streamer(TBuffer &R__b)
{
   // Stream an object of class MultiBinMaker.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      TObject::Streamer(R__b);
      R__b >> fKdBinning;
      {
         map<int,TH1*> &R__stl =  fHNInts;
         R__stl.clear();
         TClass *R__tcl2 = TBuffer::GetClass(typeid(class TH1 *));
         if (R__tcl2==0) {
            Error("fHNInts streamer","Missing the TClass object for class TH1 *!");
            return;
         }
         int R__i, R__n;
         R__b >> R__n;
         for (R__i = 0; R__i < R__n; R__i++) {
            int R__t;
            R__b >> R__t;
            TH1* R__t2;
            R__t2 = (TH1*)R__b.ReadObjectAny(R__tcl2);
            typedef int Value_t;
            std::pair<Value_t const, class TH1 * > R__t3(R__t,R__t2);
            R__stl.insert(R__t3);
         }
      }
      R__b.CheckByteCount(R__s, R__c, MultiBinMaker::IsA());
   } else {
      R__c = R__b.WriteVersion(MultiBinMaker::IsA(), kTRUE);
      TObject::Streamer(R__b);
      R__b << fKdBinning;
      {
         map<int,TH1*> &R__stl =  fHNInts;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            map<int,TH1*>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << ((*R__k).first );
            R__b << ((*R__k).second);
            }
         }
      }
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrapper around operator delete
   static void delete_MultiBinMaker(void *p) {
      delete ((::MultiBinMaker*)p);
   }
   static void deleteArray_MultiBinMaker(void *p) {
      delete [] ((::MultiBinMaker*)p);
   }
   static void destruct_MultiBinMaker(void *p) {
      typedef ::MultiBinMaker current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_MultiBinMaker(TBuffer &buf, void *obj) {
      ((::MultiBinMaker*)obj)->::MultiBinMaker::Streamer(buf);
   }
} // end of namespace ROOT for class ::MultiBinMaker

//______________________________________________________________________________
void RooMinBiasXSection::Streamer(TBuffer &R__b)
{
   // Stream an object of class RooMinBiasXSection.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      RooAbsPdf::Streamer(R__b);
      R__b >> H2d;
      R__b >> __x;
      R__b >> __xsection;
      fXSection.Streamer(R__b);
      fXVar.Streamer(R__b);
      R__b.CheckByteCount(R__s, R__c, RooMinBiasXSection::IsA());
   } else {
      R__c = R__b.WriteVersion(RooMinBiasXSection::IsA(), kTRUE);
      RooAbsPdf::Streamer(R__b);
      R__b << H2d;
      R__b << __x;
      R__b << __xsection;
      fXSection.Streamer(R__b);
      fXVar.Streamer(R__b);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_RooMinBiasXSection(void *p) {
      return  p ? new(p) ::RooMinBiasXSection : new ::RooMinBiasXSection;
   }
   static void *newArray_RooMinBiasXSection(Long_t nElements, void *p) {
      return p ? new(p) ::RooMinBiasXSection[nElements] : new ::RooMinBiasXSection[nElements];
   }
   // Wrapper around operator delete
   static void delete_RooMinBiasXSection(void *p) {
      delete ((::RooMinBiasXSection*)p);
   }
   static void deleteArray_RooMinBiasXSection(void *p) {
      delete [] ((::RooMinBiasXSection*)p);
   }
   static void destruct_RooMinBiasXSection(void *p) {
      typedef ::RooMinBiasXSection current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_RooMinBiasXSection(TBuffer &buf, void *obj) {
      ((::RooMinBiasXSection*)obj)->::RooMinBiasXSection::Streamer(buf);
   }
} // end of namespace ROOT for class ::RooMinBiasXSection

//______________________________________________________________________________
void XSectionWeight::Streamer(TBuffer &R__b)
{
   // Stream an object of class XSectionWeight.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      TObject::Streamer(R__b);
      {
         map<int,TH1*> &R__stl =  nPuData;
         R__stl.clear();
         TClass *R__tcl2 = TBuffer::GetClass(typeid(class TH1 *));
         if (R__tcl2==0) {
            Error("nPuData streamer","Missing the TClass object for class TH1 *!");
            return;
         }
         int R__i, R__n;
         R__b >> R__n;
         for (R__i = 0; R__i < R__n; R__i++) {
            int R__t;
            R__b >> R__t;
            TH1* R__t2;
            R__t2 = (TH1*)R__b.ReadObjectAny(R__tcl2);
            typedef int Value_t;
            std::pair<Value_t const, class TH1 * > R__t3(R__t,R__t2);
            R__stl.insert(R__t3);
         }
      }
      {
         vector<int> &R__stl =  availableXSecBins;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            int R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      R__b >> simNTrue;
      R__b >> xsection;
      R__b.CheckByteCount(R__s, R__c, XSectionWeight::IsA());
   } else {
      R__c = R__b.WriteVersion(XSectionWeight::IsA(), kTRUE);
      TObject::Streamer(R__b);
      {
         map<int,TH1*> &R__stl =  nPuData;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            map<int,TH1*>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << ((*R__k).first );
            R__b << ((*R__k).second);
            }
         }
      }
      {
         vector<int> &R__stl =  availableXSecBins;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<int>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      R__b << simNTrue;
      R__b << xsection;
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_XSectionWeight(void *p) {
      return  p ? new(p) ::XSectionWeight : new ::XSectionWeight;
   }
   static void *newArray_XSectionWeight(Long_t nElements, void *p) {
      return p ? new(p) ::XSectionWeight[nElements] : new ::XSectionWeight[nElements];
   }
   // Wrapper around operator delete
   static void delete_XSectionWeight(void *p) {
      delete ((::XSectionWeight*)p);
   }
   static void deleteArray_XSectionWeight(void *p) {
      delete [] ((::XSectionWeight*)p);
   }
   static void destruct_XSectionWeight(void *p) {
      typedef ::XSectionWeight current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_XSectionWeight(TBuffer &buf, void *obj) {
      ((::XSectionWeight*)obj)->::XSectionWeight::Streamer(buf);
   }
} // end of namespace ROOT for class ::XSectionWeight

//______________________________________________________________________________
void RooMultiDimCategory::Streamer(TBuffer &R__b)
{
   // Stream an object of class RooMultiDimCategory.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      RooAbsRealLValue::Streamer(R__b);
      R__b >> tkdBinning;
      {
         vector<RooRealProxy> &R__stl =  _inputVars;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            RooTemplateProxy<RooAbsReal> R__t;
            R__t.Streamer(R__b);
            R__stl.push_back(R__t);
         }
      }
      InputVars.Streamer(R__b);
      R__b >> theBinning;
      R__b.CheckByteCount(R__s, R__c, RooMultiDimCategory::IsA());
   } else {
      R__c = R__b.WriteVersion(RooMultiDimCategory::IsA(), kTRUE);
      RooAbsRealLValue::Streamer(R__b);
      R__b << tkdBinning;
      {
         vector<RooRealProxy> &R__stl =  _inputVars;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<RooRealProxy>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            ((RooTemplateProxy<RooAbsReal>&)(*R__k)).Streamer(R__b);
            }
         }
      }
      InputVars.Streamer(R__b);
      R__b << theBinning;
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_RooMultiDimCategory(void *p) {
      return  p ? new(p) ::RooMultiDimCategory : new ::RooMultiDimCategory;
   }
   static void *newArray_RooMultiDimCategory(Long_t nElements, void *p) {
      return p ? new(p) ::RooMultiDimCategory[nElements] : new ::RooMultiDimCategory[nElements];
   }
   // Wrapper around operator delete
   static void delete_RooMultiDimCategory(void *p) {
      delete ((::RooMultiDimCategory*)p);
   }
   static void deleteArray_RooMultiDimCategory(void *p) {
      delete [] ((::RooMultiDimCategory*)p);
   }
   static void destruct_RooMultiDimCategory(void *p) {
      typedef ::RooMultiDimCategory current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_RooMultiDimCategory(TBuffer &buf, void *obj) {
      ((::RooMultiDimCategory*)obj)->::RooMultiDimCategory::Streamer(buf);
   }
} // end of namespace ROOT for class ::RooMultiDimCategory

//______________________________________________________________________________
void RooNdimMinBiasXSection::Streamer(TBuffer &R__b)
{
   // Stream an object of class RooNdimMinBiasXSection.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      RooAbsPdf::Streamer(R__b);
      R__b >> MBM;
      R__b >> XSW;
      R__b >> f1DProjected;
      xsecProxy.Streamer(R__b);
      {
         vector<RooRealProxy> &R__stl =  allProxyVars;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            RooTemplateProxy<RooAbsReal> R__t;
            R__t.Streamer(R__b);
            R__stl.push_back(R__t);
         }
      }
      f1DVariable.Streamer(R__b);
      R__b.CheckByteCount(R__s, R__c, RooNdimMinBiasXSection::IsA());
   } else {
      R__c = R__b.WriteVersion(RooNdimMinBiasXSection::IsA(), kTRUE);
      RooAbsPdf::Streamer(R__b);
      R__b << MBM;
      R__b << XSW;
      R__b << f1DProjected;
      xsecProxy.Streamer(R__b);
      {
         vector<RooRealProxy> &R__stl =  allProxyVars;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<RooRealProxy>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            ((RooTemplateProxy<RooAbsReal>&)(*R__k)).Streamer(R__b);
            }
         }
      }
      f1DVariable.Streamer(R__b);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_RooNdimMinBiasXSection(void *p) {
      return  p ? new(p) ::RooNdimMinBiasXSection : new ::RooNdimMinBiasXSection;
   }
   static void *newArray_RooNdimMinBiasXSection(Long_t nElements, void *p) {
      return p ? new(p) ::RooNdimMinBiasXSection[nElements] : new ::RooNdimMinBiasXSection[nElements];
   }
   // Wrapper around operator delete
   static void delete_RooNdimMinBiasXSection(void *p) {
      delete ((::RooNdimMinBiasXSection*)p);
   }
   static void deleteArray_RooNdimMinBiasXSection(void *p) {
      delete [] ((::RooNdimMinBiasXSection*)p);
   }
   static void destruct_RooNdimMinBiasXSection(void *p) {
      typedef ::RooNdimMinBiasXSection current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_RooNdimMinBiasXSection(TBuffer &buf, void *obj) {
      ((::RooNdimMinBiasXSection*)obj)->::RooNdimMinBiasXSection::Streamer(buf);
   }
} // end of namespace ROOT for class ::RooNdimMinBiasXSection

//______________________________________________________________________________
void RooVarPDFForLumi::Streamer(TBuffer &R__b)
{
   // Stream an object of class RooVarPDFForLumi.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      RooAbsPdf::Streamer(R__b);
      R__b >> h2dSimulation;
      R__b >> lumiDist;
      R__b >> h2dVarVsXSec;
      R__b >> DeltaT;
      R__b >> __x;
      R__b >> __xsection;
      fXSection.Streamer(R__b);
      fXVar.Streamer(R__b);
      R__b.CheckByteCount(R__s, R__c, RooVarPDFForLumi::IsA());
   } else {
      R__c = R__b.WriteVersion(RooVarPDFForLumi::IsA(), kTRUE);
      RooAbsPdf::Streamer(R__b);
      R__b << h2dSimulation;
      R__b << lumiDist;
      R__b << h2dVarVsXSec;
      R__b << DeltaT;
      R__b << __x;
      R__b << __xsection;
      fXSection.Streamer(R__b);
      fXVar.Streamer(R__b);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_RooVarPDFForLumi(void *p) {
      return  p ? new(p) ::RooVarPDFForLumi : new ::RooVarPDFForLumi;
   }
   static void *newArray_RooVarPDFForLumi(Long_t nElements, void *p) {
      return p ? new(p) ::RooVarPDFForLumi[nElements] : new ::RooVarPDFForLumi[nElements];
   }
   // Wrapper around operator delete
   static void delete_RooVarPDFForLumi(void *p) {
      delete ((::RooVarPDFForLumi*)p);
   }
   static void deleteArray_RooVarPDFForLumi(void *p) {
      delete [] ((::RooVarPDFForLumi*)p);
   }
   static void destruct_RooVarPDFForLumi(void *p) {
      typedef ::RooVarPDFForLumi current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_RooVarPDFForLumi(TBuffer &buf, void *obj) {
      ((::RooVarPDFForLumi*)obj)->::RooVarPDFForLumi::Streamer(buf);
   }
} // end of namespace ROOT for class ::RooVarPDFForLumi

namespace ROOT {
   static TClass *vectorlEintgR_Dictionary();
   static void vectorlEintgR_TClassManip(TClass*);
   static void *new_vectorlEintgR(void *p = 0);
   static void *newArray_vectorlEintgR(Long_t size, void *p);
   static void delete_vectorlEintgR(void *p);
   static void deleteArray_vectorlEintgR(void *p);
   static void destruct_vectorlEintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<int>*)
   {
      vector<int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<int>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<int>", -2, "vector", 386,
                  typeid(vector<int>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlEintgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<int>) );
      instance.SetNew(&new_vectorlEintgR);
      instance.SetNewArray(&newArray_vectorlEintgR);
      instance.SetDelete(&delete_vectorlEintgR);
      instance.SetDeleteArray(&deleteArray_vectorlEintgR);
      instance.SetDestructor(&destruct_vectorlEintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<int> >()));

      ::ROOT::AddClassAlternate("vector<int>","std::vector<int, std::allocator<int> >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<int>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<int>*)0x0)->GetClass();
      vectorlEintgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEintgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int> : new vector<int>;
   }
   static void *newArray_vectorlEintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<int>[nElements] : new vector<int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEintgR(void *p) {
      delete ((vector<int>*)p);
   }
   static void deleteArray_vectorlEintgR(void *p) {
      delete [] ((vector<int>*)p);
   }
   static void destruct_vectorlEintgR(void *p) {
      typedef vector<int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<int>

namespace ROOT {
   static TClass *vectorlERooTemplateProxylERooAbsRealgRsPgR_Dictionary();
   static void vectorlERooTemplateProxylERooAbsRealgRsPgR_TClassManip(TClass*);
   static void *new_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p = 0);
   static void *newArray_vectorlERooTemplateProxylERooAbsRealgRsPgR(Long_t size, void *p);
   static void delete_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p);
   static void deleteArray_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p);
   static void destruct_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<RooTemplateProxy<RooAbsReal> >*)
   {
      vector<RooTemplateProxy<RooAbsReal> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<RooTemplateProxy<RooAbsReal> >));
      static ::ROOT::TGenericClassInfo 
         instance("vector<RooTemplateProxy<RooAbsReal> >", -2, "vector", 386,
                  typeid(vector<RooTemplateProxy<RooAbsReal> >), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &vectorlERooTemplateProxylERooAbsRealgRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<RooTemplateProxy<RooAbsReal> >) );
      instance.SetNew(&new_vectorlERooTemplateProxylERooAbsRealgRsPgR);
      instance.SetNewArray(&newArray_vectorlERooTemplateProxylERooAbsRealgRsPgR);
      instance.SetDelete(&delete_vectorlERooTemplateProxylERooAbsRealgRsPgR);
      instance.SetDeleteArray(&deleteArray_vectorlERooTemplateProxylERooAbsRealgRsPgR);
      instance.SetDestructor(&destruct_vectorlERooTemplateProxylERooAbsRealgRsPgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<RooTemplateProxy<RooAbsReal> > >()));

      ::ROOT::AddClassAlternate("vector<RooTemplateProxy<RooAbsReal> >","std::vector<RooTemplateProxy<RooAbsReal>, std::allocator<RooTemplateProxy<RooAbsReal> > >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const vector<RooTemplateProxy<RooAbsReal> >*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlERooTemplateProxylERooAbsRealgRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<RooTemplateProxy<RooAbsReal> >*)0x0)->GetClass();
      vectorlERooTemplateProxylERooAbsRealgRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlERooTemplateProxylERooAbsRealgRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<RooTemplateProxy<RooAbsReal> > : new vector<RooTemplateProxy<RooAbsReal> >;
   }
   static void *newArray_vectorlERooTemplateProxylERooAbsRealgRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) vector<RooTemplateProxy<RooAbsReal> >[nElements] : new vector<RooTemplateProxy<RooAbsReal> >[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p) {
      delete ((vector<RooTemplateProxy<RooAbsReal> >*)p);
   }
   static void deleteArray_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p) {
      delete [] ((vector<RooTemplateProxy<RooAbsReal> >*)p);
   }
   static void destruct_vectorlERooTemplateProxylERooAbsRealgRsPgR(void *p) {
      typedef vector<RooTemplateProxy<RooAbsReal> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<RooTemplateProxy<RooAbsReal> >

namespace ROOT {
   static TClass *maplEintcOTH1mUgR_Dictionary();
   static void maplEintcOTH1mUgR_TClassManip(TClass*);
   static void *new_maplEintcOTH1mUgR(void *p = 0);
   static void *newArray_maplEintcOTH1mUgR(Long_t size, void *p);
   static void delete_maplEintcOTH1mUgR(void *p);
   static void deleteArray_maplEintcOTH1mUgR(void *p);
   static void destruct_maplEintcOTH1mUgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const map<int,TH1*>*)
   {
      map<int,TH1*> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(map<int,TH1*>));
      static ::ROOT::TGenericClassInfo 
         instance("map<int,TH1*>", -2, "map", 100,
                  typeid(map<int,TH1*>), ::ROOT::Internal::DefineBehavior(ptr, ptr),
                  &maplEintcOTH1mUgR_Dictionary, isa_proxy, 0,
                  sizeof(map<int,TH1*>) );
      instance.SetNew(&new_maplEintcOTH1mUgR);
      instance.SetNewArray(&newArray_maplEintcOTH1mUgR);
      instance.SetDelete(&delete_maplEintcOTH1mUgR);
      instance.SetDeleteArray(&deleteArray_maplEintcOTH1mUgR);
      instance.SetDestructor(&destruct_maplEintcOTH1mUgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::MapInsert< map<int,TH1*> >()));

      ::ROOT::AddClassAlternate("map<int,TH1*>","std::map<int, TH1*, std::less<int>, std::allocator<std::pair<int const, TH1*> > >");
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_DICT_(Init) = GenerateInitInstanceLocal((const map<int,TH1*>*)0x0); R__UseDummy(_R__UNIQUE_DICT_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *maplEintcOTH1mUgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const map<int,TH1*>*)0x0)->GetClass();
      maplEintcOTH1mUgR_TClassManip(theClass);
   return theClass;
   }

   static void maplEintcOTH1mUgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_maplEintcOTH1mUgR(void *p) {
      return  p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<int,TH1*> : new map<int,TH1*>;
   }
   static void *newArray_maplEintcOTH1mUgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::Internal::TOperatorNewHelper*)p) map<int,TH1*>[nElements] : new map<int,TH1*>[nElements];
   }
   // Wrapper around operator delete
   static void delete_maplEintcOTH1mUgR(void *p) {
      delete ((map<int,TH1*>*)p);
   }
   static void deleteArray_maplEintcOTH1mUgR(void *p) {
      delete [] ((map<int,TH1*>*)p);
   }
   static void destruct_maplEintcOTH1mUgR(void *p) {
      typedef map<int,TH1*> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class map<int,TH1*>

namespace {
  void TriggerDictionaryInitialization_DEFS_Impl() {
    static const char* headers[] = {
"MultiBinMaker.h",
"RooMinBiasXSection.h",
"RooNdimMinBiasXSection.h",
"XSectionWeight.h",
"RooMultiDimCategory.h",
"RooVarPDFForLumi.h",
0
    };
    static const char* includePaths[] = {
"/opt/root/root_6_22/include/",
"/home/hbakhshi/Documents/PU/MainFiles/include/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "DEFS dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
class __attribute__((annotate("$clingAutoload$MultiBinMaker.h")))  MultiBinMaker;
class __attribute__((annotate("$clingAutoload$RooMinBiasXSection.h")))  RooMinBiasXSection;
class __attribute__((annotate("$clingAutoload$XSectionWeight.h")))  __attribute__((annotate("$clingAutoload$RooNdimMinBiasXSection.h")))  XSectionWeight;
class __attribute__((annotate("$clingAutoload$RooMultiDimCategory.h")))  __attribute__((annotate("$clingAutoload$RooNdimMinBiasXSection.h")))  RooMultiDimCategory;
class __attribute__((annotate("$clingAutoload$RooNdimMinBiasXSection.h")))  RooNdimMinBiasXSection;
class __attribute__((annotate("$clingAutoload$RooVarPDFForLumi.h")))  RooVarPDFForLumi;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "DEFS dictionary payload"


#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "MultiBinMaker.h"
#include "RooMinBiasXSection.h"
#include "RooNdimMinBiasXSection.h"
#include "XSectionWeight.h"
#include "RooMultiDimCategory.h"
#include "RooVarPDFForLumi.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"MultiBinMaker", payloadCode, "@",
"RooMinBiasXSection", payloadCode, "@",
"RooMultiDimCategory", payloadCode, "@",
"RooNdimMinBiasXSection", payloadCode, "@",
"RooVarPDFForLumi", payloadCode, "@",
"XSectionWeight", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("DEFS",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_DEFS_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_DEFS_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_DEFS() {
  TriggerDictionaryInitialization_DEFS_Impl();
}
