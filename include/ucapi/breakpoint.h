#ifndef UCAPI_BREAKPOINT_H_INCLUDED
#define UCAPI_BREAKPOINT_H_INCLUDED

/**
 * @brief      This function will act as a hard coded breakpoint causing the
 *             debugger to halt when connected.
 *             
 * @warning    If no debugger is connected, the behavior is undefined.
 */ 
extern void ucapi_breakpoint(void);

#endif /* UCAPI_BREAKPOINT_H_INCLUDED */
