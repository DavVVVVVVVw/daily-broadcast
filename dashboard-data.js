// dashboard-data.js — 常驻 dashboard 的数据源（模板占位版）。
// Parallight 不变要求：课程每一步都可视化。学习者每跑完一个实验，
// Mentor 就往 window.DASHBOARD 末尾 append 一条 {key,label,file,hint,code,steps}。
// HTML(tool-mechanism.html) 会自动按这个数组生成 tab —— append 时不用碰 HTML。
//
// entry schema:
//   { key:'唯一英文短名', label:'① 一句话标题', file:'对应的源文件',
//     hint:'这个实验一句话看到了什么',
//     code:[[行号, '<该行高亮 HTML>'], …],
//     steps:[{ n:'STEP 1', t:'这一步在干嘛', who:'model|you|spec', whoTxt:'谁在动手',
//              lines:[行号…], io:'<这一步真实的请求/返回/输出 HTML>' }, …] }

window.DASHBOARD = [
  { key:'start', label:'① 第一步会出现在这里', file:'(本 lab 的第一个实验)',
    hint:'学习者每跑完一个实验，Mentor 就 append 一条 entry —— 这一格会被真实内容替换。',
    code:[[1, '<span class="cmt"># 跑完第一个实验后，这里放这一步真实跑的代码行</span>']],
    steps:[{ n:'STEP 0', t:'占位：跑完第一个实验后替换我', who:'spec', whoTxt:'静态说明',
             lines:[1],
             io:'<div class="card"><div class="box">这里放这一步真实的请求 / tool_use / 返回 / stdout</div></div>' }] },
];
