#ifndef UCAPI_SYSTEM_TIMER_H_INCLUDED
#define UCAPI_SYSTEM_TIMER_H_INCLUDED

/** A type for referencing ucapi system timers. */
struct ucapi_system_timer;

/**
 * @brief      Stops the system timer.
 *
 * @param[in]  timer  The timer to be stopped.
 */
void ucapi_system_timer_stop(struct ucapi_system_timer* timer);

/**
 * @brief      Starts the system timer.
 *
 * @param[in]  timer  The timer to be started.
 */
void ucapi_system_timer_start(struct ucapi_system_timer* timer);

/**
 * @brief      Retrieves the current tick count.
 *
 * @param[in]  timer  The timer whose tick count to retrieve.
 *
 * @return     The curren tick count of the timer.
 */
unsigned int ucapi_system_timer_ticks(struct ucapi_system_timer* timer);

/**
 * @brief      Gets the number of elapsed ticks since ticks.
 *
 * @param[in]  timer  The timer of which to get the elapsed ticks.
 * @param[in]  ticks  The tick count from which on to get the elapsed ticks.
 *
 * @return     The number of elapsed ticks.
 */
unsigned int ucapi_system_timer_elapsed(struct ucapi_system_timer* timer, unsigned int ticks);

/**
 * @brief      Sets the new system timer callback and returns the callback
 *             that was previously set.
 *
 * @param      timer     The timer for which to assign the new callback.
 * @param[in]  callback  The new callback to be assigned.
 *
 * @return     The callback that was previously set.
 * @retavl     0 If no callback was previously set.
 */
void (*ucapi_system_timer_set_callback(struct ucapi_system_timer* timer, void (*callback)(void)))(void);

#endif /* UCAPI_SYSTEM_TIMER_H_INCLUDED */
