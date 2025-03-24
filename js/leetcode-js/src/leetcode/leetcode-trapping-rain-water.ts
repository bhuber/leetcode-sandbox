// https://leetcode.com/problems/trapping-rain-water/

// This solution works properly, but is not optimal
// It's O(n) time and space complexity
// Optimal is O(n) time and O(1) space, and uses completely different approach

const p = console.log;
//const p = (x: any) => {};

type Height = number;
type Idx = number

function trap(height: number[]): number {
    if (height.length === 0) {
        return 0;
    }

    // props:
    // before each loop:
    //   every height desc, every idx asc.  Ealier idx breaks ties
    //   last entry may not be valid lip, we'll find out on current iteration
    const prev_lips_desc: Array<[Height, Idx]> = [[height[0], 0]];
    let prev_height = height[0];
    let result = 0;

    for (let i = 1; i < height.length; i++) {
        let curr_height = height[i];
        p(`{i: ${i}, h: ${curr_height}, r: ${result}, pld: ${prev_lips_desc}}`);

        if (curr_height <= prev_height) {
            if (curr_height <= prev_height) {
                // Easy case: we're descending, simply push new lip onto stack
                p(`  push 1`);
                prev_lips_desc.push([curr_height, i]);
            }
            // tiebreak case
            prev_height = curr_height;
            continue;
        }

        // we're ascending
        // NOOP - we just skip loop below
        // if (prev_lips_desc.length == 0) {...}


        // add horizontal rectangles from prev_height to curr_height
        // There are n rectangles, one for each lip < curr_height on the stack
        // There may be a last partial rectangle, deal with it later
        // know we have to pop, since
        let lh = prev_height
        while (prev_lips_desc.length > 0) {
            let curr_lip = prev_lips_desc.pop()!!;
            if (curr_lip[0] > curr_height) {
                // popped too far, deal with partial rectangle
                // TODO
                let hh = curr_height;
                let pi = curr_lip[1];
                const inc = (hh - lh)*(i - pi - 1);
                p(`    {inc1: ${inc}, curr_lip: ${curr_lip}, hh: ${hh}, lh: ${lh}, pi: ${pi}`);
                result += inc;

                p(`  push 3`);
                prev_lips_desc.push(curr_lip);
                break;
            }

            let hh = curr_lip[0];
            let pi = curr_lip[1];
            const inc = (hh - lh)*(i - pi - 1);
            p(`    {inc2: ${inc}, curr_lip: ${curr_lip}, hh: ${hh}, lh: ${lh}, pi: ${pi}`);
            result += inc;

            lh = hh;
        }

        prev_lips_desc.push([curr_height, i]);
        p(`  push 2`);

        prev_height = curr_height;
    }

    p(`{r: ${result}, pld: ${prev_lips_desc}}`);

    return result;
};