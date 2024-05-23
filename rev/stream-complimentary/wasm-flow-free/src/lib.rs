mod utils;
use rand::{seq::IteratorRandom, thread_rng, Rng};
use std::{
    cmp::{max, min},
    collections::{HashMap, HashSet},
    convert::TryInto,
    num::NonZeroUsize,
};
use wasm_bindgen::prelude::*;
const SPRITE_SIZE: i32 = 40;
const SPRITE_SCALE: i32 = 1;
const FLOW_SIZE: i32 = SPRITE_SIZE * SPRITE_SCALE;
const BORDER_SIZE: i32 = 1;
const BORDER_FILL: u16 = 0xccc;

#[wasm_bindgen]
extern "C" {
    // Use `js_namespace` here to bind `console.log(..)` instead of just
    // `log(..)`
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
#[repr(u8)]
pub enum Flow {
    Dot = 2,
    Line = 1,
    Empty = 0,
}

#[derive(Clone, Copy, Debug)]
pub struct Fill {
    color: u16,
    flow: Flow,
    dirs: [bool; 4],
    // left, right, up, down
    // if all true, then dot
}

impl Fill {
    pub fn new(color: u16, flow: Flow, dirs: [bool; 4]) -> Self {
        Self { color, flow, dirs }
    }
}

#[derive(Clone, Debug)]
pub struct Board {
    pub width: i32,
    pub height: i32,
    pub fills: Vec<Fill>,
}

#[wasm_bindgen]
extern "C" {
    fn alert(s: &str);
}

impl Board {
    pub fn new(width: i32, height: i32) -> Self {
        utils::set_panic_hook();
        let fills = vec![Fill::new(0x000, Flow::Empty, [false; 4]); (width * height) as usize];
        Self {
            width,
            height,
            fills,
        }
    }

    pub fn get_fill(&self, x: i32, y: i32) -> Fill {
        self.fills[(y * self.width + x) as usize]
    }

    pub fn set_fill(&mut self, x: i32, y: i32, fill: Fill) {
        self.fills[(y * self.width + x) as usize] = fill;
    }
    fn adjacent(&self, pos_a: i32, pos_b: i32) -> bool {
        pos_a >= 0
            && pos_a < self.width * self.height
            && pos_b >= 0
            && pos_b < self.width * self.height
            && ((pos_a % self.width) - (pos_b % self.width)).abs() <= 1
            && ((pos_a / self.width) as i32 - (pos_b / self.width) as i32).abs() <= 1
    }
    pub fn add_connection(&mut self, pos_a: i32, pos_b: i32) -> bool {
        if !self.adjacent(pos_a, pos_b) {
            return false;
        }
        let fill_a = self.fills[pos_a as usize];
        let fill_b = self.fills[pos_b as usize];
        // precondition: A already is a line/dot
        if let Flow::Empty = fill_a.flow {
            return false;
        } else if let Flow::Empty = fill_b.flow {
            // if B is empty, we'll give it the same color as A
        } else if fill_a.color != fill_b.color {
            return false;
        }

        // dots should only have one connection, lines can have two, empty will have one
        for fill in [fill_a, fill_b] {
            if fill.dirs.iter().filter(|b| **b).count()
                >= match fill.flow {
                    Flow::Empty => 1,
                    Flow::Dot => 1,
                    Flow::Line => 2,
                }
            {
                return false;
            }
        }

        let delta = pos_b - pos_a;
        let my_pos = match delta {
            -1 => 0,                        // left
            1 => 1,                         // right
            _ if delta == -self.width => 2, // up
            _ if delta == self.width => 3,  // down
            _ => panic!("Invalid delta"),
        };
        let their_pos = [1, 0, 3, 2][my_pos as usize]; // opposite of my_pos

        // actually add connection between A and B
        let new_fill_a = Fill {
            color: fill_a.color,
            flow: fill_a.flow,
            dirs: {
                let mut new_dirs_a = match fill_a.flow {
                    Flow::Empty => [false; 4],
                    _ => fill_a.dirs,
                };
                new_dirs_a[my_pos] = true;
                new_dirs_a
            },
        };
        let new_fill_b = Fill {
            color: match fill_b.flow {
                Flow::Empty => fill_a.color,
                _ => fill_b.color,
            },
            flow: match fill_b.flow {
                Flow::Empty => Flow::Line,
                _ => fill_b.flow,
            },
            dirs: {
                let mut new_dirs_b = match fill_b.flow {
                    Flow::Empty => [false; 4],
                    _ => fill_b.dirs,
                };
                new_dirs_b[their_pos] = true;
                new_dirs_b
            },
        };
        self.fills[pos_a as usize] = new_fill_a;
        self.fills[pos_b as usize] = new_fill_b;
        return true;
    }
    // for consistency with add_connection, pos_a will be the one that gets removed
    fn remove_connection(&mut self, pos_a: i32, pos_b: i32) -> bool {
        if !self.adjacent(pos_a, pos_b) {
            return false;
        }
        let fill_a = self.fills[pos_a as usize];
        let fill_b = self.fills[pos_b as usize];
        // precondition: both are not empty, fill_a is not a dot, and both are same color
        if let Flow::Empty = fill_a.flow {
            return false;
        } else if let Flow::Dot = fill_a.flow {
            return false;
        }
        if let Flow::Empty = fill_b.flow {
            return false;
        }
        if fill_a.color != fill_b.color {
            return false;
        }
        let delta = pos_b - pos_a;
        let my_pos = match delta {
            -1 => 0,                        // left
            1 => 1,                         // right
            _ if delta == -self.width => 2, // up
            _ if delta == self.width => 3,  // down
            _ => panic!("Invalid delta"),
        };
        let other_pos = [1, 0, 3, 2][my_pos as usize]; // opposite of my_pos
        let new_fill_a = Fill {
            color: 0x000,
            flow: Flow::Empty,
            dirs: [false; 4],
        };
        let new_fill_b = Fill {
            color: fill_b.color,
            flow: fill_b.flow,
            dirs: {
                let mut new_dirs_b = fill_b.dirs;
                new_dirs_b[other_pos] = false;
                new_dirs_b
            },
        };
        self.fills[pos_a as usize] = new_fill_a;
        self.fills[pos_b as usize] = new_fill_b;

        true
    }

    fn clear_pipe(&mut self, pos: i32) {
        match self.fills[pos as usize].flow {
            Flow::Dot => (),
            _ => return,
        }
        let deltas = [-1, 1, -self.width, self.width];
        let fill_start = self.fills[pos as usize];
        let explored = &mut vec![false; (self.width * self.height) as usize];
        let mut to_explore: Vec<i32> = Vec::new();
        to_explore.push(pos);
        while let Some(entry) = to_explore.pop() {
            if explored[entry as usize] {
                continue;
            }
            explored[entry as usize] = true;
            let this_fill = self.fills[entry as usize];
            for (i, &delta) in deltas.iter().enumerate() {
                if this_fill.dirs[i] == false {
                    continue;
                }
                let new_pos = entry + delta;
                if new_pos < 0
                    || new_pos >= self.width * self.height
                    || !self.adjacent(entry, new_pos)
                    || explored[new_pos as usize]
                    || fill_start.color != self.fills[new_pos as usize].color
                {
                    continue;
                }
                // if not connected
                let my_pos = match delta {
                    -1 => 0,                        // left
                    1 => 1,                         // right
                    _ if delta == -self.width => 2, // up
                    _ if delta == self.width => 3,  // down
                    _ => panic!("Invalid delta"),
                };

                let their_pos = [1, 0, 3, 2][my_pos as usize]; // opposite of my_pos
                if !(this_fill.dirs[my_pos] && self.fills[new_pos as usize].dirs[their_pos]) {
                    continue;
                }

                to_explore.push(new_pos);
            }
            if let Flow::Dot = self.fills[entry as usize].flow {
                self.fills[entry as usize].dirs = [false; 4];
            } else {
                self.fills[entry as usize] = Fill::new(0x00, Flow::Empty, [false; 4]);
            }
        }
    }

    fn is_connected(&self, pos_a: i32, pos_b: i32) -> bool {
        let fill_a = self.fills[pos_a as usize];
        let deltas = [-1, 1, -self.width, self.width];
        let explored = &mut vec![false; (self.width * self.height) as usize];
        let mut to_explore: Vec<i32> = Vec::new();
        to_explore.push(pos_a);
        while let Some(entry) = to_explore.pop() {
            if explored[entry as usize] {
                continue;
            } // probably redundant, but it's better to check
            if entry == pos_b {
                return true;
            }
            explored[entry as usize] = true;

            let this_fill = self.fills[entry as usize];

            for (i, &delta) in deltas.iter().enumerate() {
                if this_fill.dirs[i] == false {
                    continue;
                }
                let new_pos = entry + delta;
                if new_pos < 0
                    || new_pos >= self.width * self.height
                    || !self.adjacent(entry, new_pos)
                    || explored[new_pos as usize]
                    || fill_a.color != self.fills[new_pos as usize].color
                {
                    continue;
                }
                // if not connected
                let my_pos = match delta {
                    -1 => 0,                        // left
                    1 => 1,                         // right
                    _ if delta == -self.width => 2, // up
                    _ if delta == self.width => 3,  // down
                    _ => panic!("Invalid delta"),
                };
                let their_pos = [1, 0, 3, 2][my_pos as usize]; // opposite of my_pos
                if !(this_fill.dirs[my_pos] && self.fills[new_pos as usize].dirs[their_pos]) {
                    continue;
                }

                to_explore.push(new_pos);
            }
        }
        false
    }

    fn check_all_connected(&self) -> bool {
        let mut pairs: HashMap<u16, Vec<i32>> = HashMap::new();
        for i in 0..(self.width * self.height) {
            let fill = self.fills[i as usize];
            if let Flow::Dot = fill.flow {
                if !pairs.contains_key(&fill.color) {
                    pairs.insert(fill.color, Vec::new());
                }

                pairs.get_mut(&fill.color).unwrap().push(i);
            }
        }
        for pair in pairs.values() {
            if pair.len() != 2 {
                continue;
            }
            let (start, end) = (pair[0], pair[1]);
            if !self.is_connected(start, end) {
                return false;
            }
        }
        true
    }

    fn fully_filled(&self) -> bool {
        for i in 0..(self.width * self.height) as usize {
            if let Flow::Empty = self.fills[i].flow {
                return false;
            }
        }
        true
    }

    /*
    u32 width
    u32 height

    [u32; width*height] fill:
        bits 0-4: dirs (left, right, up, down)
        bits 5-6: flow type (Dot = 2, Line = 1, Empty = 0)
        bits 7-18: color (4 bits per color)
        bits 22-31: reserved for future use

    */
    fn write_board(&self) -> Vec<u8> {
        let mut serialized: Vec<u8> = Vec::new();
        serialized.extend(self.width.to_be_bytes().iter());
        serialized.extend(self.height.to_be_bytes().iter());
        for fill in &self.fills {
            let mut fill_data = 0;
            for (i, &dir) in fill.dirs.iter().enumerate() {
                if dir {
                    fill_data |= 1 << i;
                }
            }
            fill_data |= match fill.flow {
                Flow::Empty => 0 << 5,
                Flow::Line => 1 << 5,
                Flow::Dot => 2 << 5,
            };
            fill_data |= (fill.color as u32 & 0xfff) << 7;
            serialized.extend(fill_data.to_be_bytes().iter());
        }
        serialized
    }

    fn read_board(serialized: &[u32]) -> Self {
        let width = serialized[0].try_into().expect("Board too wide");
        let height = serialized[1].try_into().expect("Board too high");
        let mut board = Board::new(width, height);
        if width * height != (serialized.len() - 2) as i32 {
            panic!("Invalid board size");
        }
        for i in 2..serialized.len() {
            let dirs = [
                (serialized[i] & 0b1) != 0,
                (serialized[i] & 0b10) != 0,
                (serialized[i] & 0b100) != 0,
                (serialized[i] & 0b1000) != 0,
            ];
            let flow = match (serialized[i] >> 5) & 0b11 {
                0 => Flow::Empty,
                1 => Flow::Line,
                2 => Flow::Dot,
                _ => panic!("Invalid flow type"),
            };
            let color = (serialized[i] >> 7) & 0xfff;
            board.fills[i - 2] = Fill::new(color as u16, flow, dirs);
        }
        board
    }
}

#[wasm_bindgen]
pub struct Canvas {
    board: Board,
    pix_buf: Vec<u8>,
    current_pzl: Option<u8>,
}

#[wasm_bindgen]
impl Canvas {
    fn set_pix(buf: &mut [u8], loc: usize, color: u32) {
        buf[loc * 4] = ((color >> 24) & 0xff) as u8; // red
        buf[loc * 4 + 1] = ((color >> 16) & 0xff) as u8; // green
        buf[loc * 4 + 2] = ((color >> 8) & 0xff) as u8; // blue
        buf[loc * 4 + 3] = (color & 0xff) as u8; // alpha should just be 255 hopefully
    }

    fn unpack_color(input: u16) -> u32 {
        let r = (((input >> 8) & 0xf) << 4) as u32;
        let g = (((input >> 4) & 0xf) << 4) as u32;
        let b = (((input >> 0) & 0xf) << 4) as u32;
        r << 24 | g << 16 | b << 8 | 0xff
    }

    pub fn new(width: i32, height: i32) -> Self {
        let board = Board::new(width, height);
        let total_width = board.width * FLOW_SIZE + (board.width - 1) * BORDER_SIZE;
        let total_height = board.height * FLOW_SIZE + (board.height - 1) * BORDER_SIZE;
        let mut pix_buf = (0..((total_width * total_height * 4) as usize))
            .map(|i| if i % 4 == 3 { 0xff } else { 0 })
            .collect::<Vec<u8>>();

        for y in 0..total_height {
            for x in 0..total_width {
                if x % (FLOW_SIZE + BORDER_SIZE) >= FLOW_SIZE
                    || y % (FLOW_SIZE + BORDER_SIZE) >= FLOW_SIZE
                {
                    Self::set_pix(
                        &mut pix_buf,
                        (y * total_width + x) as usize,
                        Canvas::unpack_color(BORDER_FILL),
                    );
                }
            }
        }
        Self {
            board,
            pix_buf,
            current_pzl: None,
        }
    }

    pub fn new_chall() -> Self {
        let mut canvas = Self::new(1, 1);
        canvas.current_pzl = Some(0);
        canvas.load_puzzle(0);
        canvas
    }

    fn render_flow(&mut self, fill: Fill, x: i32, y: i32) {
        let sprite: &[u8; (SPRITE_SIZE * SPRITE_SIZE) as usize] = match fill.flow {
            Flow::Dot => match fill.dirs {
                [false, false, false, false] => include_bytes!("sprites/0"),
                [true, false, false, false] => include_bytes!("sprites/1"),
                [false, true, false, false] => include_bytes!("sprites/2"),
                [false, false, true, false] => include_bytes!("sprites/3"),
                [false, false, false, true] => include_bytes!("sprites/4"),
                _ => panic!("Invalid flow"),
            },
            Flow::Empty => include_bytes!("sprites/5"),
            Flow::Line => match fill.dirs {
                [true, false, false, false] => include_bytes!("sprites/6"),
                [false, true, false, false] => include_bytes!("sprites/7"),
                [false, false, true, false] => include_bytes!("sprites/8"),
                [false, false, false, true] => include_bytes!("sprites/9"),
                [false, true, true, false] => include_bytes!("sprites/10"),
                [false, true, false, true] => include_bytes!("sprites/11"),
                [true, false, false, true] => include_bytes!("sprites/12"),
                [true, false, true, false] => include_bytes!("sprites/13"),
                [false, false, true, true] => include_bytes!("sprites/14"),
                [true, true, false, false] => include_bytes!("sprites/15"),
                _ => panic!("Invalid flow"),
            },
        };
        let start_x = x * (FLOW_SIZE + BORDER_SIZE);
        let start_y = y * (FLOW_SIZE + BORDER_SIZE);
        for y in 0..FLOW_SIZE {
            for x in 0..FLOW_SIZE {
                let scale = sprite[((y / SPRITE_SCALE) * SPRITE_SIZE + x / SPRITE_SCALE) as usize]
                    as f32
                    / 255.0;

                let pix_r = ((((fill.color >> 8) & 0xf) as f32 * scale) as u32) << 4;
                let pix_g = ((((fill.color >> 4) & 0xf) as f32 * scale) as u32) << 4;
                let pix_b = ((((fill.color >> 0) & 0xf) as f32 * scale) as u32) << 4;

                let color = pix_r << 24 | pix_g << 16 | pix_b << 8 | 0xff;
                let pos = ((start_y + y) * (self.canvas_width()) + start_x + x) as usize;
                Self::set_pix(&mut self.pix_buf, pos, color);
            }
        }
    }
    pub fn render(&mut self) {
        for y in 0..self.board.height {
            for x in 0..self.board.width {
                let fill = self.board.fills[(y * self.board.width + x) as usize];
                self.render_flow(fill, x, y);
            }
        }
    }

    pub fn get_pix_buf(&self) -> *const u8 {
        self.pix_buf.as_ptr() as *const u8
    }

    pub fn width(&self) -> i32 {
        self.board.width
    }

    pub fn height(&self) -> i32 {
        self.board.height
    }
    pub fn canvas_height(&self) -> i32 {
        self.board.height * FLOW_SIZE + (self.board.height - 1) * BORDER_SIZE
    }
    pub fn canvas_width(&self) -> i32 {
        self.board.width * FLOW_SIZE + (self.board.width - 1) * BORDER_SIZE
    }

    pub fn box_at(&self, x: i32, y: i32) -> Option<Vec<i32>> {
        let x_pos = x / (FLOW_SIZE + BORDER_SIZE);
        let y_pos = y / (FLOW_SIZE + BORDER_SIZE);
        if x_pos >= FLOW_SIZE || y_pos >= FLOW_SIZE {
            return None;
        }
        Some([x / (FLOW_SIZE + BORDER_SIZE), y / (FLOW_SIZE + BORDER_SIZE)].into())
    }

    pub fn clear_pipe(&mut self, pos: Vec<i32>) {
        if pos.len() != 2 {
            return;
        }
        let pos = pos[1] * self.board.width + pos[0];
        self.board.clear_pipe(pos);
    }

    pub fn add_connection(&mut self, pos: Vec<i32>, delta: i32) -> bool {
        if pos.len() != 2 {
            return false;
        }
        let pos = pos[1] * self.board.width + pos[0];
        let other_pos = pos
            + match delta {
                0 => -1,
                1 => 1,
                2 => -self.board.width,
                3 => self.board.width,
                _ => return false,
            };
        let res = self.board.add_connection(pos, other_pos);
        if res {
            if let Some(pzl) = self.current_pzl {
                // assume a parity bit in pos 7
                if self.game_won() {
                    if (pzl.count_ones() & 1) == 0 {
                        let pzl = (pzl & !(1 << 7)) + 1;
                        self.load_puzzle(pzl);
                        self.current_pzl = Some(pzl | ((pzl.count_ones() & 1) << 7) as u8);
                    } else {
                        self.current_pzl = Some(0);
                        self.load_puzzle(0);
                    }
                }
            }
            true
        } else {
            false
        }
    }
    pub fn remove_connection(&mut self, pos: Vec<i32>, delta: i32) -> bool {
        if pos.len() != 2 {
            return false;
        }
        let pos = pos[1] * self.board.width + pos[0];
        let other_pos = pos
            + match delta {
                0 => -1,
                1 => 1,
                2 => -self.board.width,
                3 => self.board.width,
                _ => return false,
            };
        self.board.remove_connection(pos, other_pos)
    }

    // fn check_all_connected(&self) -> bool {
    //     self.board.check_all_connected()
    // }

    pub fn game_won(&self) -> bool {
        self.board.fully_filled() && self.board.check_all_connected()
    }

    fn write_board(&self) -> Vec<u8> {
        self.board.write_board()
    }

    fn read_board(&mut self, serialized: &[u32]) {
        let board = Board::read_board(serialized);
        self.board = board;
    }

    pub fn gen_filled_board(width: i32, height: i32) -> Self {
        /*
        https://doug-osborne.com/the-level-generator/
        Same color dots are never next to each other (corollary:  all lines are at least 3 tiles long, including the endpoints).
        The no “zig-zag” rule, which informally means that lines can’t have unnecessary bends in them.
        Here’s one way to explicitly define the no “zig-zag” rule:
        If a line could have entered a square at an earlier point but didn’t, it can’t ever enter that square.
        */
        const MIN_LINE_LENGTH: i32 = 2;
        let max_line_length = if width + height < 20 {
            width * height / 4
        } else {
            (width + height) * 2
        };
        let mut canvas = Canvas::new(width, height);
        let mut candidates = Vec::new();
        let gen_candidates: usize = match width + height {
            ..=16 => 3000,
            17..=19 => 1000,
            20..=36 => 200,
            37.. => 5,
        };
        for _ in 0..gen_candidates {
            let mut board = Board::new(width, height);
            loop {
                let mut used_by: Vec<Option<NonZeroUsize>> = vec![None; (width * height) as usize];
                // let mut used_by: Vec<i32> = vec![-1; (width * height) as usize];
                let mut dots: Vec<usize> = Vec::new();
                let mut filled = 0;
                let mut rng = thread_rng();
                let deltas = [-1, 1, -width, width];
                let mut failed_fills = 0; // number of sequential "short" fills
                while filled < (width * height) && failed_fills < 10 {
                    let start_pos =
                        (rand::random::<u32>() % ((width * height) - filled) as u32) as i32;
                    let start_pos = (0..(width * height) as usize)
                        .filter(|&i| used_by[i].is_none())
                        .nth(start_pos as usize)
                        .unwrap() as i32; // bounded between 0 and # available, so this can never fail
                    let mut last_used = start_pos;
                    let mut visited = vec![false; (width * height) as usize]; // all locations the path could have visited
                    visited[start_pos as usize] = true;
                    let ideal_length = min(
                        rng.gen_range(max(MIN_LINE_LENGTH, max_line_length / 4)..max_line_length),
                        width * height - filled,
                    );
                    let pipe_id = (dots.len() / 2) + 1;
                    for _ in 0..ideal_length {
                        if filled >= width * height {
                            break;
                        }
                        // log("called loop");
                        let possible_nbrs = deltas
                            .iter()
                            .filter(|&delta| {
                                let new_pos = last_used as i32 + delta;
                                canvas.board.adjacent(last_used, new_pos)
                                    && !visited[new_pos as usize]
                                    && used_by[new_pos as usize].is_none()
                            })
                            .map(|i| last_used as i32 + i)
                            .collect::<Vec<i32>>();
                        for &nbr in possible_nbrs.iter() {
                            visited[nbr as usize] = true;
                        }
                        if let Some(&nbr) = possible_nbrs.iter().choose(&mut rng) {
                            used_by[nbr as usize] = Some(NonZeroUsize::new(pipe_id).unwrap());
                            // used_by[nbr as usize] = start_pos;
                            filled += 1;
                            last_used = nbr;
                        } else {
                            break;
                        }
                    }

                    if last_used != start_pos {
                        filled += 1;
                        failed_fills = 0;
                        used_by[start_pos as usize] = Some(NonZeroUsize::new(pipe_id).unwrap());
                        // used_by[start_pos as usize] = start_pos;
                        dots.push(start_pos as usize);
                        dots.push(last_used as usize);
                    } else {
                        failed_fills += 1;
                    }
                }

                // try to extend lines to fill blank spaces
                // the number of passes is arbitrary, but it ought to be enough
                const FILL_PASSES: usize = 5;
                for _ in 0..FILL_PASSES {
                    let blanks = (0..(width * height) as usize)
                        .filter(|i| used_by[*i].is_none())
                        .collect::<Vec<usize>>();
                    for blank in blanks {
                        let possible_nbrs = deltas
                            .iter()
                            .filter(|&delta| {
                                let new_pos = blank as i32 + delta;
                                board.adjacent(blank as i32, new_pos)
                                    && used_by[new_pos as usize].is_some()
                                    && dots.contains(&(new_pos as usize))
                            })
                            .map(|i| blank as i32 + i);
                        let (mut dot_choice, mut best_pipe_ct) = (None, None);
                        for nbr in possible_nbrs {
                            if let Some(pos) = dots.iter().position(|&x| x == nbr as usize) {
                                let id = NonZeroUsize::new(pos / 2 + 1);
                                let this_pipe_ct =
                                    used_by.iter().filter(|&&elem| elem == id).count() as usize;
                                if let Some(pipe_ct) = best_pipe_ct {
                                    if pipe_ct < this_pipe_ct {
                                        best_pipe_ct = Some(this_pipe_ct);
                                        dot_choice = Some(pos);
                                    }
                                } else {
                                    dot_choice = Some(pos);
                                    best_pipe_ct = Some(this_pipe_ct);
                                }
                            }
                        }
                        if let Some(dot_choice) = dot_choice {
                            used_by[blank] = Some(NonZeroUsize::new(dot_choice / 2 + 1).unwrap());
                            dots[dot_choice] = blank as usize;
                        }
                    }
                }
                if used_by.iter().all(|&b| b.is_some()) {
                    let palette = get_color_palette((dots.len() / 2) as i32);
                    for i in 0..(width * height) {
                        board.set_fill(
                            i % width,
                            i / width,
                            Fill::new(
                                palette[used_by[i as usize].unwrap().get() - 1],
                                match dots.contains(&(i as usize)) {
                                    true => Flow::Dot,
                                    false => Flow::Line,
                                },
                                [false; 4],
                            ),
                        );
                    }
                    // add connections to appropriate adjacent spots
                    for i in 0..(width * height) {
                        let deltas = [-1, 1, -width, width];
                        for &delta in deltas.iter() {
                            let new_pos = i + delta;
                            if board.adjacent(i, new_pos) && used_by[new_pos as usize].is_some() {
                                board.add_connection(i, new_pos);
                            }
                        }
                    }

                    // # of short pipes
                    let short_pipe_score: i32 = used_by
                        .iter()
                        .filter(|&&elem| {
                            elem.is_some() && used_by.iter().filter(|&&x| x == elem).count() <= 2
                        })
                        .count() as i32;

                    let pipe_compact_score: i32 = (0..dots.len())
                        .step_by(2)
                        .map(|i| {
                            let start = dots[i];
                            let end = dots[i + 1];
                            let start_x = start as i32 % width;
                            let start_y = start as i32 / width;
                            let end_x = end as i32 % width;
                            let end_y = end as i32 / width;
                            let id = NonZeroUsize::new(i / 2 + 1);
                            let total_pipe_len =
                                used_by.iter().filter(|&&elem| elem == id).count() as i32;
                            total_pipe_len / ((start_x - end_x).abs() + (start_y - end_y).abs())
                        })
                        .sum();
                    let pipe_dist_score: i32 = (0..dots.len())
                        .step_by(2)
                        .map(|i| {
                            let start = dots[i];
                            let end = dots[i + 1];
                            let start_x = start as i32 % width;
                            let start_y = start as i32 / width;
                            let end_x = end as i32 % width;
                            let end_y = end as i32 / width;

                            (start_x - end_x).abs() + (start_y - end_y).abs()
                        })
                        .sum();
                    let num_flows_score = dots.len() as i32 / 2;
                    let adjacent_dots_score: i32 = (0..dots.len())
                        .step_by(2)
                        .map(|i| board.adjacent(dots[i] as i32, dots[i + 1] as i32) as i32)
                        .sum();
                    // number of 2x2 squares (bad)
                    let square_offsets = [0, 1, width, width + 1];
                    let two_squares_score = (0..height - 1)
                        .map(|y| {
                            (0..width - 1)
                                .map(|x| {
                                    square_offsets.iter().all(|&offset| {
                                        let pos = (y * width + x) + offset;
                                        used_by[pos as usize] == used_by[(y * width + x) as usize]
                                    }) as i32
                                })
                                .sum::<i32>()
                        })
                        .sum::<i32>();
                    // candidate with LOWEST score is chosen
                    let this_candidate_score = 0
                        + 64 * short_pipe_score
                        + -1 * pipe_dist_score
                        + -2 * pipe_compact_score
                        + 8 * num_flows_score
                        + 64 * adjacent_dots_score
                        + 32 * two_squares_score;
                    candidates.push((this_candidate_score, board));
                    break;
                }
            }
        }
        canvas.board = candidates
            .iter()
            .min_by_key(|(score, _)| *score)
            .unwrap()
            .1
            .clone();
        canvas
    }

    pub fn clear_all_flows(&mut self) {
        for x in 0..self.board.width {
            for y in 0..self.board.height {
                let is_dot = match self.board.get_fill(x, y).flow {
                    Flow::Dot => true,
                    _ => false,
                };
                self.board.set_fill(
                    x,
                    y,
                    Fill::new(
                        if is_dot {
                            self.board.get_fill(x, y).color
                        } else {
                            0x000
                        },
                        if is_dot { Flow::Dot } else { Flow::Empty },
                        [false; 4],
                    ),
                );
            }
        }
    }
    pub fn gen_new_board(width: i32, height: i32) -> Self {
        let mut canvas = Canvas::gen_filled_board(width, height);
        canvas.clear_all_flows();
        canvas
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        self.write_board()
    }

    pub fn from_bytes(&mut self, board: &[u8]) {
        if let Some(_) = self.current_pzl {
            self.current_pzl = None;
        }
        if (board.len()) % 4 != 0 {
            return;
        }
        if u32::from_be_bytes(board[0..4].try_into().unwrap()) != self.board.width as u32
            || u32::from_be_bytes(board[4..8].try_into().unwrap()) != self.board.height as u32
        {
            return;
        }

        self.read_board(
            (0..board.len())
                .step_by(4)
                .map(|i| u32::from_be_bytes(board[i..(i + 4)].try_into().unwrap()))
                .collect::<Vec<u32>>()
                .as_slice(),
        );
    }

    pub fn resize(&mut self, width: i32, height: i32) {
        if let Some(_) = self.current_pzl {
            self.current_pzl = None;
        }
        let new_canvas = Canvas::new(width, height);
        self.board = new_canvas.board;
        self.pix_buf = new_canvas.pix_buf;
    }

    pub fn add_dot_at(&mut self, x: i32, y: i32, color: u16) {
        if let Some(_) = self.current_pzl {
            self.current_pzl = None;
        }
        if (x < 0 || x >= self.board.width) || (y < 0 || y >= self.board.height) {
            return;
        }
        let old_fill = self.board.get_fill(x, y);
        if old_fill.dirs.iter().filter(|v| **v).count() >= 2 {
            return;
        }
        self.board
            .set_fill(x, y, Fill::new(color, Flow::Dot, old_fill.dirs));
    }

    pub fn remove_dot_at(&mut self, x: i32, y: i32) {
        if let Some(_) = self.current_pzl {
            self.current_pzl = None;
        }
        self.board.clear_pipe(y * self.board.width + x);
        self.board
            .set_fill(x, y, Fill::new(0x000, Flow::Empty, [false; 4]));
    }

    pub fn remap_color_palette(&mut self, new_palette: Option<Vec<u16>>) {
        let current_palette = self
            .board
            .fills
            .iter()
            .filter(|fill| match fill.flow {
                Flow::Dot => true,
                _ => false,
            })
            .map(|fill| fill.color)
            .collect::<HashSet<u16>>();
        let num_colors = current_palette.len();
        let new_palette = match new_palette {
            Some(palette) => palette,
            None => get_color_palette(num_colors as i32),
        };
        if new_palette.len() < num_colors {
            return;
        }
        for fill in self.board.fills.iter_mut() {
            match fill.flow {
                Flow::Empty => (),
                _ => {
                    let new_color = new_palette[current_palette
                        .iter()
                        .position(|&x| x == fill.color)
                        .unwrap()];
                    fill.color = new_color;
                }
            };
        }
    }
    fn load_puzzle(&mut self, number: u8) {
        let (data, width, height): (Vec<u8>, i32, i32) = match number {
            0 => (include_bytes!("puzzles/0_5x5").into(), 5, 5),
            1 => (include_bytes!("puzzles/1_5x5").into(), 5, 5),
            2 => (include_bytes!("puzzles/2_6x6").into(), 6, 6),
            3 => (include_bytes!("puzzles/3_6x6").into(), 6, 6),
            4 => (include_bytes!("puzzles/4_7x7").into(), 7, 7),
            5 => (include_bytes!("puzzles/5_7x7").into(), 7, 7),
            6 => (include_bytes!("puzzles/6_8x8").into(), 8, 8),
            7 => (include_bytes!("puzzles/7_9x9").into(), 9, 9),
            8 => (include_bytes!("puzzles/8_3x3").into(), 3, 3),
            9 => (include_bytes!("puzzles/9_140x15").into(), 140, 15),
            _ => return,
        };
        let old_current_pzl = self.current_pzl;
        self.resize(width, height);
        self.from_bytes(&data);
        self.current_pzl = old_current_pzl;
    }

    pub fn get_puzzle_type(&self) -> String {
        match self.current_pzl {
            None => "Free play".into(),
            Some(i) => format!("Level {}/10", (i & !(1 << 7)) + 1),
        }
    }
}

#[wasm_bindgen]
pub fn get_color_palette(size: i32) -> Vec<u16> {
    const CLASSIC_COLORS: [u16; 8] = [0xf00, 0xff0, 0x13f, 0x0a0, 0xa33, 0xfa0, 0x0ff, 0xf0c];
    const CONTRAST_COLORS: [u16; 25] = [
        0xfaf, 0x7d, 0x930, 0x405, 0x053, 0x2c4, 0xfc9, 0x888, 0x9fb, 0x870, 0x9c0, 0xc08, 0x038,
        0xfa0, 0xfab, 0x460, 0xf01, 0x5ff, 0x098, 0xef6, 0x70f, 0x900, 0xff8, 0xff0, 0xf50,
    ];
    let mut rng = thread_rng();
    if size < CLASSIC_COLORS.len() as i32 {
        CLASSIC_COLORS[0..size as usize].to_vec()
    } else if size < CONTRAST_COLORS.len() as i32 {
        CONTRAST_COLORS
            .iter()
            .choose_multiple(&mut rng, size as usize)
            .iter()
            .map(|&&x| x)
            .collect()
    } else {
        let mut colors = Vec::with_capacity(size as usize);
        loop {
            for _ in colors.len()..size as usize {
                let red = rng.gen_range(4..16);
                let green = rng.gen_range(4..16);
                let blue = rng.gen_range(4..16);
                colors.push((red << 8) | (green << 4) | blue);
            }
            colors.sort();
            colors.dedup();
            if colors.len() == size as usize {
                break;
            }
        }
        colors
    }
}
