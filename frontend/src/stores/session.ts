import type {User} from '../types/domain';
export function readUser():User|null{try{return JSON.parse(localStorage.getItem('queue-user')||'null')}catch{return null}}
export function save(token:string,user:User){localStorage.setItem('queue-token',token);localStorage.setItem('queue-user',JSON.stringify(user))}
export function clear(){localStorage.removeItem('queue-token');localStorage.removeItem('queue-user')}
