#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _NEWAXNODE_reg(void);
extern void _xtra_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," NEWAXNODE.mod");
    fprintf(stderr," xtra.mod");
    fprintf(stderr, "\n");
  }
  _NEWAXNODE_reg();
  _xtra_reg();
}
