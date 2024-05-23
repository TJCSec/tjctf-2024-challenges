FROM oven/bun@sha256:c28304be3943868463e2acf9f595f640c6e0e069e0b0782e4804e1781187b4ec
COPY . .
RUN bun install

ENTRYPOINT ["bun", "run", "app.js"]
