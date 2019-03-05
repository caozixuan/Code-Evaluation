
public class test1 {



    public int count = 0;    //用于计算遍历总次数
    /*
     * adjMatrix是待遍历图的邻接矩阵
     * value是待遍历图顶点用于是否被遍历的判断依据，0代表未遍历，非0代表已被遍历
     * result用于存放深度优先遍历的顶点顺序
     */
    public void dfs(int[][] adjMatrix,int[] value,char[] result){
        for(int i = 0;i < value.length;i++){
            if(value[i] == 0){
                char temp = (char) ('a' + i);
                System.out.println();
                System.out.println("深度为："+i+"，当前出发点："+temp);
                result[i] = temp;                //存放当前正在遍历顶点下标字母
                dfsVisit(adjMatrix,value,result,i);
            }
        }
    }
    /*
     * adjMatrix是待遍历图的邻接矩阵
     * value是待遍历图顶点用于是否被遍历的判断依据，0代表未遍历，非0代表已被遍历
     * result用于存放深度优先遍历的顶点顺序
     * number是当前正在遍历的顶点在邻接矩阵中的数组下标编号
     */
    public void dfsVisit(int[][] adjMatrix,int[] value,char[] result,int number){
        value[number] = ++count;               //把++count赋值给当前正在遍历顶点判断值数组元素，变为非0，代表已被遍历
        System.out.print("当前已行走顶点value["+number+"] = "+value[number]+"  ");
        for(int i = 0;i < value.length;i++){
            if(adjMatrix[number][i] == 1 && value[i] == 0){          //当当前顶点的相邻有相邻顶点可行走且其为被遍历
                char temp = (char) ('a' + i);
                result[count] = temp;        //存放即将行走的顶点下标字母
                System.out.println(" 当前i值："+i+" 到达"+temp+"地");
                dfsVisit(adjMatrix,value,result,i);   //执行递归，行走第i个顶点
            }
        }
    }

    public static void main(String[] args){
        int[] value = new int[10];              //初始化后，各元素均为0
        char[] result = new char[10];
        int[][] adjMatrix = {{0,0,1,1,1,0,0,0,0,0},
                {0,0,0,0,1,1,0,0,0,0},
                {1,0,0,1,0,1,0,0,0,0},
                {1,0,1,0,0,0,0,0,0,0},
                {1,1,0,0,0,1,0,0,0,0},
                {0,1,1,0,1,0,0,0,0,0},
                {0,0,0,0,0,0,0,1,0,1},
                {0,0,0,0,0,0,1,0,1,0},
                {0,0,0,0,0,0,0,1,0,1},
                {0,0,0,0,0,0,1,0,1,0}};
        test1 test = new test1();
        test.dfs(adjMatrix,value,result);
        System.out.println();
        System.out.println("判断节点是否被遍历结果（0代表未遍历，非0代表已被遍历）：");
        for(int i = 0;i < value.length;i++)
            System.out.print("  "+value[i]);
        System.out.println();
        System.out.println("深度优先查找遍历顺序如下：");
        for(int i = 0;i < result.length;i++)
            System.out.print("  "+result[i]);
    }
}