/*
 * Instance header file for ATSAMD11D14AU
 *
 * Copyright (c) 2025 Microchip Technology Inc. and its subsidiaries.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

/* file generated from device description file (ATDF) version 2025-07-18T12:13:11Z */
#ifndef _SAMD11_TCC0_INSTANCE_
#define _SAMD11_TCC0_INSTANCE_


/* ========== Instance Parameter definitions for TCC0 peripheral ========== */
#define TCC0_CC_NUM                              (4)        /* Number of Compare/Capture units */
#define TCC0_DITHERING                           (1)        /* Dithering feature implemented */
#define TCC0_DMAC_ID_MC0                         (8)        /* DMA Match/Compare 0 trigger */
#define TCC0_DMAC_ID_MC1                         (9)        /* DMA Match/Compare 1 trigger */
#define TCC0_DMAC_ID_MC2                         (10)       /* DMA Match/Compare 2 trigger */
#define TCC0_DMAC_ID_MC3                         (11)       /* DMA Match/Compare 3 trigger */
#define TCC0_DMAC_ID_OVF                         (7)        /* DMA overflow/underflow/retrigger trigger */
#define TCC0_DTI                                 (1)        /* Dead-Time-Insertion feature implemented */
#define TCC0_EXT                                 (31)       /* (@_DITHERING*16+@_PG*8+@_SWAP*4+@_DTI*2+@_OTMX*1) */
#define TCC0_GCLK_ID                             (17)       /* Index of Generic Clock */
#define TCC0_INSTANCE_ID                         (69)
#define TCC0_MASTER                              (0)
#define TCC0_OTMX                                (1)        /* Output Matrix feature implemented */
#define TCC0_OW_NUM                              (8)        /* Number of Output Waveforms */
#define TCC0_PG                                  (1)        /* Pattern Generation feature implemented */
#define TCC0_SIZE                                (24)
#define TCC0_SWAP                                (1)        /* DTI outputs swap feature implemented */

#endif /* _SAMD11_TCC0_INSTANCE_ */
