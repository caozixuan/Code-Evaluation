
public class test3 {



    //n表示的是定义全排列的位数，可以根据题目意思和实际情况自行输入自行定义
    public static int n=3;
    public static char a[]=new char[4];    //存储结果的数组的大小
    public static int book[]=new int[95];  //大写字母的ASCII码值在65-91
    public static void main(String[] args)
    {
        dfs(1);
    }

    private static void dfs(int temp)
    {
        if(temp==n+1)
        {
            System.out.printf("%c%c%c  \n",a[1],a[2],a[3]);
            return;
        }
        for(int i='A';i<='C';i++)  //也可以使用ASCII码在做i的取值范围
        {
            if(book[i]==0)
            {
                a[temp]=(char)i;
                book[i]=1;
                dfs(temp+1);
                book[i]=0;
            }
        }
        return;

    }
}