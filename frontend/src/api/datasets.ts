import {request,post} from './client';import type {Dataset,DatasetRevision} from '../types/domain';
export const list=()=>request<Dataset[]>('/datasets');
export const create=(data:unknown)=>post<Dataset>('/datasets',data);
export const updateObservations=(id:string,data:unknown)=>post<Dataset>('/datasets/'+id+'/observations',data);
export const revisions=(id:string)=>request<DatasetRevision[]>('/datasets/'+id+'/revisions');
