export const number=(v:number|null|undefined,d=2)=>v==null?'不可估计':v.toFixed(d);
export const percent=(v:number|null|undefined)=>v==null?'无稳态':(v*100).toFixed(1)+'%';
export const date=(v:string)=>new Date(v).toLocaleString('zh-CN',{hour12:false});
