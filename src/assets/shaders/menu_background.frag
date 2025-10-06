#version 330

uniform vec2 iResolution;
uniform vec4 base_color = vec4(0.08, 0.08, 0.12, 1.0);
uniform vec4 accent_color = vec4(0.9, 0.6, 0.2, 1.0);
uniform float time = 0.0;

in vec2 uv;
out vec4 fragColor;

void main() {
    vec2 pos = uv * iResolution;
    float aspect = iResolution.x / iResolution.y;

    // vertical gradient
    float g = smoothstep(0.0, 1.0, uv.y);
    vec3 color = mix(base_color.rgb, base_color.rgb * 1.2, g);

    // subtle moving stripes for texture
    float stripes = 0.02 * sin((uv.x + time * 0.05) * 40.0) + 0.02 * cos((uv.y + time * 0.03) * 60.0);
    color += stripes * 0.5;

    // vignette
    vec2 centered = uv - 0.5;
    centered.x *= aspect;
    float dist = length(centered);
    color *= smoothstep(0.8, 0.4, dist);

    // accent rim at top
    float rim = exp(-pow((uv.y - 0.05) * 20.0, 2.0));
    color = mix(color, accent_color.rgb, rim * 0.25);

    fragColor = vec4(color, base_color.a);
}
