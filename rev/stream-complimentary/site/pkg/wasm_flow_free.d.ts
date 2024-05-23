/* tslint:disable */
/* eslint-disable */
/**
* @param {number} size
* @returns {Uint16Array}
*/
export function get_color_palette(size: number): Uint16Array;
/**
*/
export class Canvas {
  free(): void;
/**
* @param {number} width
* @param {number} height
* @returns {Canvas}
*/
  static new(width: number, height: number): Canvas;
/**
* @returns {Canvas}
*/
  static new_chall(): Canvas;
/**
*/
  render(): void;
/**
* @returns {number}
*/
  get_pix_buf(): number;
/**
* @returns {number}
*/
  width(): number;
/**
* @returns {number}
*/
  height(): number;
/**
* @returns {number}
*/
  canvas_height(): number;
/**
* @returns {number}
*/
  canvas_width(): number;
/**
* @param {number} x
* @param {number} y
* @returns {Int32Array | undefined}
*/
  box_at(x: number, y: number): Int32Array | undefined;
/**
* @param {Int32Array} pos
*/
  clear_pipe(pos: Int32Array): void;
/**
* @param {Int32Array} pos
* @param {number} delta
* @returns {boolean}
*/
  add_connection(pos: Int32Array, delta: number): boolean;
/**
* @param {Int32Array} pos
* @param {number} delta
* @returns {boolean}
*/
  remove_connection(pos: Int32Array, delta: number): boolean;
/**
* @returns {boolean}
*/
  game_won(): boolean;
/**
* @param {number} width
* @param {number} height
* @returns {Canvas}
*/
  static gen_filled_board(width: number, height: number): Canvas;
/**
*/
  clear_all_flows(): void;
/**
* @param {number} width
* @param {number} height
* @returns {Canvas}
*/
  static gen_new_board(width: number, height: number): Canvas;
/**
* @returns {Uint8Array}
*/
  to_bytes(): Uint8Array;
/**
* @param {Uint8Array} board
*/
  from_bytes(board: Uint8Array): void;
/**
* @param {number} width
* @param {number} height
*/
  resize(width: number, height: number): void;
/**
* @param {number} x
* @param {number} y
* @param {number} color
*/
  add_dot_at(x: number, y: number, color: number): void;
/**
* @param {number} x
* @param {number} y
*/
  remove_dot_at(x: number, y: number): void;
/**
* @param {Uint16Array | undefined} [new_palette]
*/
  remap_color_palette(new_palette?: Uint16Array): void;
/**
* @returns {string}
*/
  get_puzzle_type(): string;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly __wbg_canvas_free: (a: number) => void;
  readonly canvas_new: (a: number, b: number) => number;
  readonly canvas_new_chall: () => number;
  readonly canvas_render: (a: number) => void;
  readonly canvas_get_pix_buf: (a: number) => number;
  readonly canvas_width: (a: number) => number;
  readonly canvas_height: (a: number) => number;
  readonly canvas_canvas_height: (a: number) => number;
  readonly canvas_canvas_width: (a: number) => number;
  readonly canvas_box_at: (a: number, b: number, c: number, d: number) => void;
  readonly canvas_clear_pipe: (a: number, b: number, c: number) => void;
  readonly canvas_add_connection: (a: number, b: number, c: number, d: number) => number;
  readonly canvas_remove_connection: (a: number, b: number, c: number, d: number) => number;
  readonly canvas_game_won: (a: number) => number;
  readonly canvas_gen_filled_board: (a: number, b: number) => number;
  readonly canvas_clear_all_flows: (a: number) => void;
  readonly canvas_gen_new_board: (a: number, b: number) => number;
  readonly canvas_to_bytes: (a: number, b: number) => void;
  readonly canvas_from_bytes: (a: number, b: number, c: number) => void;
  readonly canvas_resize: (a: number, b: number, c: number) => void;
  readonly canvas_add_dot_at: (a: number, b: number, c: number, d: number) => void;
  readonly canvas_remove_dot_at: (a: number, b: number, c: number) => void;
  readonly canvas_remap_color_palette: (a: number, b: number, c: number) => void;
  readonly canvas_get_puzzle_type: (a: number, b: number) => void;
  readonly get_color_palette: (a: number, b: number) => void;
  readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly __wbindgen_malloc: (a: number, b: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_exn_store: (a: number) => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {SyncInitInput} module
*
* @returns {InitOutput}
*/
export function initSync(module: SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {InitInput | Promise<InitInput>} module_or_path
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: InitInput | Promise<InitInput>): Promise<InitOutput>;
