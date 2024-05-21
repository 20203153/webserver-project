import { defineNuxtPlugin } from '#app';

import mdit from 'markdown-it';
import mditHighlightjs from 'markdown-it-highlightjs';

export default defineNuxtPlugin(nuxtApp => {
    const renderer = mdit();
    renderer.use(mditHighlightjs);

    return {
        provide: {
            mdRenderer: renderer
        }
    }
});