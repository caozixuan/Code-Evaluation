
public class test4 {




    static int a[]=new int[10];
    static int book[]=new int[10];
    static int n=9;
    static int count=0;
    public static void main(String[] args)
    {
        dfs(1);
        System.out.println(count/2/3);  //注意此处需要将count除以3除以二，思路中已经解释原因
    }

    private static void dfs(int temp)
    {
        if(temp==n+1)
        {
            int a1=a[1]+a[2]+a[3]+a[4];
            int b1=a[4]+a[5]+a[6]+a[7];
            int c1=a[7]+a[8]+a[9]+a[1];
            if(a1==b1  && b1==c1)   //将三条边两两相等
            {
                count++;
            }
            return;
        }
        for(int i=1;i<=9;i++)
        {
            if(book[i]==0)
            {
                a[temp]=i;
                book[i]=1;
                dfs(temp+1);
                book[i]=0;
            }
        }
        return;
    }

}