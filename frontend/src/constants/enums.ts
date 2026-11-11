export const ROLES:Record<string,string>={admin:'管理员',analyst:'容量分析员',viewer:'只读复核员'};
export const RUN_STATUS:Record<string,string>={queued:'排队中',running:'仿真中',completed:'已完成',failed:'失败'};
export const PERIODS:Record<string,string>={all:'全日',peak:'高峰',offpeak:'平峰'};
export const DECISIONS:Record<string,string>={accepted:'接受并记录假设',needs_attention:'需要继续核查'};
