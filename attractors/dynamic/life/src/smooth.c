#define nil NULL

void smooth_scene(SDL_Surface *pixmap) {
    SDL_Surface* tmp = SDL_ConvertSurface(pixmap, pixmap->format, SDL_SWSURFACE);
    Uint8 *src;
    Uint8 *dst;
    int x, y;
    int srcc_offset;

    SDL_FillRect(pixmap, nil, 0x00);
    dst = (Uint8*)pixmap->pixels + 1*pixmap->pitch + 1*pixmap->format->BytesPerPixel;
    src = (Uint8*)tmp->pixels;

    srcc_offset = tmp->pitch-3*tmp->format->BytesPerPixel;

    for (y=1; y<tmp->h; y++) {
        for (x=1; x<tmp->w-1; x++) {
            Uint8 *srcc=src + (x-1)*tmp->format->BytesPerPixel;
            int rr=0, gg=0, bb=0;
            int dx, dy;
            for (dy=-1; dy<=1; dy++) {
                for (dx=-1; dx<=1; dx++) {
                    bb+=*srcc++;
                    gg+=*srcc++;
                    rr+=*srcc++;
                    if (tmp->format->BytesPerPixel==4) {
                        srcc++;
                    }
                }
                srcc+=srcc_offset;
            }
            rr/=9;
            gg/=9;
            bb/=9;
            *dst++ = bb;
            *dst++ = gg;
            *dst++ = rr;
            if (pixmap->format->BitsPerPixel == 32) {
                dst++;
            }
        }
        dst+=2*pixmap->format->BytesPerPixel;
        src+=tmp->pitch;
    }
}
