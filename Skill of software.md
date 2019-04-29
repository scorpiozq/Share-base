- ### 解决GitHub的卡顿问题  
  打开hosts文件：C:\Windows\System32\drivers\etc  
可以用文本文档打开，然后在最后一行加入下面几句：  
192.30.252.123 http://www.github.com  
103.245.222.133 http://assets-cdn.github.com  
185.31.18.133 http://avatars0.githubusercontent.com  
185.31.19.133 http://avatars1.githubusercontent.com  
保存关闭，重启浏览器即可。
