import { getcyElements} from './cytoscape_script.js' 

/**
 * Puts all arguments into one JSON which is then returned
 */
function put_JSON_together(graph, search, end)
{
    return {
        graph: graph,
        search: search,
        end: end
    }
}

/**
 * Puts all arguments and elements of cytoscapes into one JSON
 * @param {*} search_strat1 
 * @param {*} search_strat2 
 * @param {*} end_strat1 
 * @param {*} end_strat2 
 * @returns 
 */
export function create_json_of_graphs(search_strat1, search_strat2, end_strat1, end_strat2)
{
    let cy1Data = getcyElements(false);
    let cy2Data = getcyElements(true);
    let cy1JSON = put_JSON_together(cy1Data, search_strat1.value, end_strat1.value);
    let cy2JSON = put_JSON_together(cy2Data, search_strat2.value, end_strat2.value);
    let final_json = {
        part_one: cy1JSON,
        part_two: cy2JSON
    }
    return JSON.stringify(final_json);
}