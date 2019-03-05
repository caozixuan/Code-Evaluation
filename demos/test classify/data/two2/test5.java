
public class test5 {


    static int[] a = new int[10];
    static int count = 0;
    static int[] book = new int[10];
    static int n = 9;

    public static void main(String[] args) {
        dfs(1);
        System.out.println(count + "个");
    }

    private static void dfs(int stem) {
        if (stem == n + 1) {
            if (a[1] + a[2] * 1.0 / a[3] + (a[4] * 100 + a[5] * 10 + a[6]) * 1.0 / (a[7] * 100 + a[8] * 10 + a[9]) == 10) {
                count++;
                System.out.printf("%d + %d/%d + %d%d%d/%d%d%d =10   \n",
                        a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]);
            }
            return;
        }
        for (int i = 1; i <= 9; i++) {
            if (book[i] == 0)   //代表判断的这个数没有被标记，也就是还没有排列
            {
                a[stem] = i;
                book[i] = 1;
                dfs(stem + 1);
                book[i] = 0;    //取消标记1
            }
        }
        return;

    }
}