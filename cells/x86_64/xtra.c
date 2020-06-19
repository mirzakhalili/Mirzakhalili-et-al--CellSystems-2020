/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__xtra
#define _nrn_initial _nrn_initial__xtra
#define nrn_cur _nrn_cur__xtra
#define _nrn_current _nrn_current__xtra
#define nrn_jacob _nrn_jacob__xtra
#define nrn_state _nrn_state__xtra
#define _net_receive _net_receive__xtra 
#define f f__xtra 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define rx1 _p[0]
#define rx2 _p[1]
#define x _p[2]
#define y _p[3]
#define z _p[4]
#define er _p[5]
#define _g _p[6]
#define im	*_ppvar[0]._pval
#define _p_im	_ppvar[0]._pval
#define ex	*_ppvar[1]._pval
#define _p_ex	_ppvar[1]._pval
#define area	*_ppvar[2]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  0;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_f(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_xtra", _hoc_setdata,
 "f_xtra", _hoc_f,
 0, 0
};
 /* declare global and static user variables */
#define is2 is2_xtra
 double is2 = 0;
#define is1 is1_xtra
 double is1 = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "is1_xtra", "milliamp",
 "is2_xtra", "milliamp",
 "rx1_xtra", "megohm",
 "rx2_xtra", "megohm",
 "x_xtra", "1",
 "y_xtra", "1",
 "z_xtra", "1",
 "er_xtra", "microvolts",
 "im_xtra", "milliamp/cm2",
 "ex_xtra", "millivolts",
 0,0
};
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "is1_xtra", &is1_xtra,
 "is2_xtra", &is2_xtra,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"xtra",
 "rx1_xtra",
 "rx2_xtra",
 "x_xtra",
 "y_xtra",
 "z_xtra",
 0,
 "er_xtra",
 0,
 0,
 "im_xtra",
 "ex_xtra",
 0};
 extern Node* nrn_alloc_node_;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 7, _prop);
 	/*initialize range parameters*/
 	rx1 = 1;
 	rx2 = 1;
 	x = 0;
 	y = 0;
 	z = 0;
 	_prop->param = _p;
 	_prop->param_size = 7;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 	_ppvar[2]._pval = &nrn_alloc_node_->_area; /* diam */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _xtra_reg() {
	int _vectorized = 0;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 7, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "pointer");
  hoc_register_dparam_semantics(_mechtype, 1, "pointer");
  hoc_register_dparam_semantics(_mechtype, 2, "area");
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 xtra /home/mirzakh/TI/cells/x86_64/xtra.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int f();
 
static int  f (  ) {
   ex = is1 * rx1 * ( 1e6 ) + is2 * rx2 * ( 1e6 ) ;
   er = ( 10.0 ) * rx1 * im * area + ( 10.0 ) * rx2 * im * area ;
    return 0; }
 
static void _hoc_f(void) {
  double _r;
   _r = 1.;
 f (  );
 hoc_retpushx(_r);
}

static void initmodel() {
  int _i; double _save;_ninits++;
{
 {
   ex = is1 * rx1 * ( 1e6 ) + is2 * rx2 * ( 1e6 ) ;
   er = ( 10.0 ) * rx1 * im * area + ( 10.0 ) * rx2 * im * area ;
   }

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{
} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {
   ex = is1 * rx1 * ( 1e6 ) + is2 * rx2 * ( 1e6 ) ;
   er = ( 10.0 ) * rx1 * im * area + ( 10.0 ) * rx2 * im * area ;
   }
}}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/home/mirzakh/TI/cells/xtra.mod";
static const char* nmodl_file_text = 
  "COMMENT\n"
  "This mechanism is intended to be used in conjunction \n"
  "with the extracellular mechanism.  Pointers specified \n"
  "at the hoc level must be used to connect the \n"
  "extracellular mechanism's e_extracellular and i_membrane \n"
  "to this mechanism's ex and im, respectively.\n"
  "\n"
  "xtra does three useful things:\n"
  "\n"
  "1. Serves as a target for Vector.play() to facilitate \n"
  "extracellular stimulation.  Assumes that one has initialized \n"
  "a Vector to hold the time sequence of the stimulus current.\n"
  "This Vector is to be played into the GLOBAL variable is \n"
  "(GLOBAL so only one Vector.play() needs to be executed), \n"
  "which is multiplied by the RANGE variable rx (\"transfer \n"
  "resistance between the stimulus electrode and the local \n"
  "node\").  This product, called ex in this mechanism, is the \n"
  "extracellular potential at the local node, i.e. is used to \n"
  "drive local e_extracellular.\n"
  "\n"
  "2. Reports the contribution of local i_membrane to the \n"
  "total signal that would be picked up by an extracellular \n"
  "recording electrode.  This is computed as the product of rx, \n"
  "i_membrane (called im in this mechanism), and the surface area \n"
  "of the local segment, and is reported as er.  The total \n"
  "extracellularly recorded potential is the sum of all er_xtra \n"
  "over all segments in all sections, and is to be computed at \n"
  "the hoc level, e.g. with code like\n"
  "\n"
  "func fieldrec() { local sum\n"
  "  sum = 0\n"
  "  forall {\n"
  "    if (ismembrane(\"xtra\")) {\n"
  "      for (x) sum += er_xtra(x)\n"
  "    }\n"
  "  }\n"
  "  return sum\n"
  "}\n"
  "\n"
  "Bipolar recording, i.e. recording the difference in potential \n"
  "between two extracellular electrodes, can be achieved with no \n"
  "change to either this NMODL code or fieldrec(); the values of \n"
  "rx will reflect the difference between the potentials at the \n"
  "recording electrodes caused by the local membrane current, so \n"
  "some rx will be negative and others positive.  The same rx \n"
  "can be used for bipolar stimulation.\n"
  "\n"
  "Multiple monopolar or bipolar extracellular recording and \n"
  "stimulation can be accommodated by changing this mod file to \n"
  "include additional rx, er, and is, and changing fieldrec() \n"
  "to a proc.\n"
  "\n"
  "3. Allows local storage of xyz coordinates interpolated from \n"
  "the pt3d data.  These coordinates are used by hoc code that \n"
  "computes the transfer resistance that couples the membrane \n"
  "to extracellular stimulating and recording electrodes.\n"
  "\n"
  "\n"
  "Prior to NEURON 5.5, the SOLVE statement in the BREAKPOINT block \n"
  "used METHOD cvode_t so that the adaptive integrators wouldn't miss \n"
  "the stimulus.  Otherwise, the BREAKPOINT block would have been called \n"
  "_after_ the integration step, rather than from within cvodes/ida, \n"
  "causing this mechanism to fail to deliver a stimulus current \n"
  "when the adaptive integrator is used.\n"
  "\n"
  "With NEURON 5.5 and later, this mechanism abandons the BREAKPOINT \n"
  "block and uses the two new blocks BEFORE BREAKPOINT and  \n"
  "AFTER BREAKPOINT, like this--\n"
  "\n"
  "BEFORE BREAKPOINT { : before each cy' = f(y,t) setup\n"
  "  ex = is*rx*(1e6)\n"
  "}\n"
  "AFTER SOLVE { : after each solution step\n"
  "  er = (10)*rx*im*area\n"
  "}\n"
  "\n"
  "This ensures that the stimulus potential is computed prior to the \n"
  "solution step, and that the recorded potential is computed after.\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX xtra\n"
  "	RANGE rx1,rx2, er\n"
  "	RANGE x, y, z\n"
  "	GLOBAL is1,is2\n"
  "	POINTER im, ex\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	: default transfer resistance between stim electrodes and axon\n"
  "	rx1 = 1 (megohm) : mV/nA\n"
  "	rx2 = 1 (megohm) : mV/nA\n"
  "	x = 0 (1) : spatial coords\n"
  "	y = 0 (1)\n"
  "	z = 0 (1)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (millivolts)\n"
  "	is1 (milliamp)\n"
  "	is2 (milliamp)\n"
  "	ex (millivolts)\n"
  "	im (milliamp/cm2)\n"
  "	er (microvolts)\n"
  "	area (micron2)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	ex = is1*rx1*(1e6)+is2*rx2*(1e6)\n"
  "	er = (10)*rx1*im*area+(10)*rx2*im*area\n"
  ": this demonstrates that area is known\n"
  ": UNITSOFF\n"
  ": printf(\"area = %f\\n\", area)\n"
  ": UNITSON\n"
  "}\n"
  "\n"
  ": Use BREAKPOINT for NEURON 5.4 and earlier\n"
  ": BREAKPOINT {\n"
  ":	SOLVE f METHOD cvode_t\n"
  ": }\n"
  "\n"
  ": With NEURON 5.5 and later, abandon the BREAKPOINT block\n"
  ": and instead use BEFORE BREAKPOINT and AFTER BREAKPOINT\n"
  "\n"
  "BREAKPOINT { : before each cy' = f(y,t) setup\n"
  "  ex = is1*rx1*(1e6)+is2*rx2*(1e6)\n"
  "\n"
  "  er = (10)*rx1*im*area+(10)*rx2*im*area\n"
  "}\n"
  "\n"
  "PROCEDURE f() {\n"
  "	: 1 mA * 1 megohm is 1000 volts\n"
  "	: but ex is in mV\n"
  "	ex = is1*rx1*(1e6)+is2*rx2*(1e6)\n"
  "	er = (10)*rx1*im*area+(10)*rx2*im*area\n"
  "}\n"
  ;
#endif
