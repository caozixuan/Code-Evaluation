
public class test10 {


    static int[] book= {0,0,0,0,0,0,0,0,0,0,0};
    static int sum=0,i;
    static int e[][]={{0,0,0,0,0,0},
            {0,0,1,1,99,1},
            {0,1,0,99,1,99},
            {0,1,99,0,99,1},
            {0,99,1,99,0,99},
            {0,1,99,1,99,0}};
    public static void main(String[] args){
        book[1]=1;
        dfs(1);
    }
    public static void dfs(int k){
        System.out.print(k);
        sum++;
        if(sum==5) return;
        for(i=1;i<=5;i++){
            if(e[k][i]==1&&book[i]==0){
                book[i]=1;
                dfs(i);
            }
        }
        //return;

    }
    }



