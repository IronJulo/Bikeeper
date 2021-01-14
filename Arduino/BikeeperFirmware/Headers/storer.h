#ifndef STORER_H
#define STORER_H

void 
storeInt3(int value, char *into);

void 
storeInt4(int value, char *into);

void
storeSignedDouble(double value, int width, int precision, char *into);

void
storeSignedInt4(int value, char *into);
#endif