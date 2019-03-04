#ifndef UCAPI_DEBUG_H_INCLUDED
#define UCAPI_DEBUG_H_INCLUDED

enum ucapi_debug_states
{
    ucapi_debug_enabled,
    ucapi_debug_disabled,
    ucapi_debug_unknown,
};

/**
 * @brief      If possible this function checks whether the system is being
 *             debugged or if it is running free.
 *
 * @retval     ucapi_debug_enabled The system is being debugged.
 * @retval     ucapi_debug_disabled The system is running free.
 * @retval     ucapi_debug_unknown The debug state cannot be determined.
 */
extern enum ucapi_debug_states ucapi_get_debug_state(void);

#endif /* UCAPI_DEBUG_H_INCLUDED */