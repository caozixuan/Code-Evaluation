import java.util.Scanner;

public class test2 {



    static int m,n;   //静态变量m表示城市的个数,n表示总路线的条数
    static int e[][]=new int[101][101];
    static int book[]=new int[101];   //标记数组，主要在后面标记已走过的路线，防止重复
    static int min=999999;
    public static void main(String[] args)
    {
        Scanner s=new Scanner(System.in);
        m=s.nextInt();   //表示城市的个数
        n=s.nextInt();   //表示总路线
        int a,b,c;
        //有m个城市，所以建立一个m*m的矩阵
        for(int i=1;i<=m;i++)
        {
            for(int j=1;j<=m;j++)
            {
                if(i==j)
                    e[i][j]=0;  //每个城市到每个城市之间的距离为0
                else
                    e[i][j]=min;   //也就是初始化为无限大的数
            }
        }
        for(int i=1;i<=n;i++)
        {
            a=s.nextInt();
            b=s.nextInt();
            c=s.nextInt();   //城市与城市之间的距离
            e[a][b]=c;     //存储到二维数组中(也就是转换后的矩阵中)
        }
        dfs(1,0);   //从第一个城市出发，记录步数从0开始
        System.out.println(min);
    }
    private static void dfs(int sta, int temp)
    {
        if(sta==5)     //此处的5也就是到达第五个城市
        {
            if(min>temp)
                min=temp;
            return;
        }
        for(int i=1;i<=5;i++)
        {
            if(e[sta][i]!=min && book[i]==0)
            {
                book[i]=1;   //对走过的路线进行标记
                dfs(i,temp+e[sta][i]);
                book[i]=0;
            }
        }
        return;
    }

}