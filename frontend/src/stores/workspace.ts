import * as datasets from '../api/datasets';import * as profiles from '../api/profiles';import * as scenarios from '../api/scenarios';import * as runs from '../api/runs';import * as reviews from '../api/reviews';import * as reports from '../api/reports';import * as audit from '../api/audit';
export async function load(){const [d,p,s,r,v,o,a]=await Promise.all([datasets.list(),profiles.list(),scenarios.list(),runs.list(),reviews.list(),reports.list(),audit.list()]);return {datasets:d,profiles:p,scenarios:s,runs:r,reviews:v,reports:o,audit:a}}
export type Workspace=Awaited<ReturnType<typeof load>>;
export const emptyWorkspace=():Workspace=>({datasets:[],profiles:[],scenarios:[],runs:[],reviews:[],reports:[],audit:[]});
