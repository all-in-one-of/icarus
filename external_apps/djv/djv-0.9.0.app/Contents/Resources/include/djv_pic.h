//------------------------------------------------------------------------------
// Copyright (c) 2004-2012 Darby Johnston
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above copyright notice,
//   this list of conditions, and the following disclaimer.
//
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions, and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
//
// * Neither the names of the copyright holders nor the names of any
//   contributors may be used to endorse or promote products derived from this
//   software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
//------------------------------------------------------------------------------

//! \file djv_pic.h

#ifndef DJV_PIC_H
#define DJV_PIC_H

#include <djv_string.h>

//!\namespace djv_pic
//
//! This plugin provides support for the Softimage image file format.
//!
//! Supports:
//!
//! - Read-only
//! - Images: 8-bit, RGB, RGBA, RGB plus Alpha
//! - File compression
//!
//! References:
//!
//! - Softimage, "INFO: PIC file format"
//!   http://xsi.wiki.avid.com/index.php/INFO:_PIC_file_format

namespace djv_pic
{
using namespace djv;

static const String name = "PIC";

static const List<String> extensions = List<String>() <<
    ".pic";

//! Type.

enum TYPE
{
    TYPE_RGB,
    TYPE_RGBA,
    TYPE_RGB_A,

    _TYPE_SIZE
};

//! Compression.

enum COMPRESSION
{
    COMPRESSION_NONE,
    COMPRESSION_RLE,

    _COMPRESSION_SIZE
};

//! Get the compression labels.

const List<String> & label_compression();

//! Load RLE data.

const uint8_t * rle_load(
    const uint8_t * in,
    const uint8_t * end,
    uint8_t *       out,
    int             size,
    int             channels,
    int             stride,
    bool            endian);

} // djv_pic

#endif // DJV_PIC_H

