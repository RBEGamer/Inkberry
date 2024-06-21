/**
 **************************************************
 *
 * @file        Inkplate7.h
 * @brief       Basic funtions for controling Inkplate 7
 *
 *              https://github.com/SolderedElectronics/Inkplate-Arduino-library
 *              For more info about the product, please check: www.inkplate.io
 *
 *              This code is released under the GNU Lesser General Public
 *License v3.0: https://www.gnu.org/licenses/lgpl-3.0.en.html Please review the
 *LICENSE file included with this example. If you have any questions about
 *licensing, please contact techsupport@e-radionica.com Distributed as-is; no
 *warranty is given.
 *
 * @authors     Robert @ Soldered
 ***************************************************/

#ifndef INKPLATE_INKBERRY_H
#define INKPLATE_INKBERRY_H

#define EPAPER_RST_PIN  19
#define EPAPER_DC_PIN   33
#define EPAPER_CS_PIN   27
#define EPAPER_BUSY_PIN 32 
#define EPAPER_CLK      18
#define EPAPER_DIN      23

#define BUSY_TIMEOUT_MS 1000

// ePaper specific defines
#define E_INK_HEIGHT    480
#define E_INK_WIDTH     800
#define INKPLATE_INKBERRY_WHITE 0
#define INKPLATE_INKBERRY_BLACK 1
#define INKPLATE_INKBERRY_RED   2

// Pin on the internal io expander which controls MOSFET for turning on and off the SD card
#define SD_PMOS_PIN IO_PIN_B2 // 10

#define IO_INT_ADDR 0x20
#define IO_EXT_ADDR 0x20

#ifndef _swap_int16_t
#define _swap_int16_t(a, b)                                                                                            \
    {                                                                                                                  \
        int16_t t = a;                                                                                                 \
        a = b;                                                                                                         \
        b = t;                                                                                                         \
    }
#endif

#endif
