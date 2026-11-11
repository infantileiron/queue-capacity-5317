import {request,post} from './client';import type {Profile} from '../types/domain';
export const list=()=>request<Profile[]>('/profiles');
export const create=(data:unknown)=>post<Profile>('/profiles',data);
