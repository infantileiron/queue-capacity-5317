import {request,post} from './client';import type {Scenario} from '../types/domain';
export const list=()=>request<Scenario[]>('/scenarios');
export const create=(data:unknown)=>post<Scenario>('/scenarios',data);
export const acknowledge=(id:string)=>post<Scenario>('/scenarios/'+id+'/acknowledge',{});
