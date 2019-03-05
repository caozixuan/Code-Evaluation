public class test8 {
    private int[][] adjMat;
    //private int size;
    private Vertex[] vertexArr;
    private int num;
    private StackGraph sg;
    public static void main(String[] args) {
        test8 g = new test8(5);
        g.addVertex('A');
        g.addVertex('B');
        g.addVertex('C');
        g.addVertex('D');
        g.addVertex('E');
        g.addVertex('F');
        g.addEdge(0, 1);
        g.addEdge(0, 2);
        g.addEdge(1, 3);
        g.addEdge(2, 3);
        g.addEdge(0, 4);
        g.showGraph();
        System.out.print("visits:");
        g.dfs();
        //System.out.println();
    }
    public test8(int s){
        //size = s;
        num = 0;
        adjMat = new int[s][s];
        vertexArr = new Vertex[s];
        for(int i=0;i<s;i++){
            for(int j=0;j<s;j++){
                adjMat[i][j] = 0;
            }
        }
        sg = new StackGraph(s);
    }
    public void addVertex(char c){
        if(num<5){
            Vertex nVertex = new Vertex();
            nVertex.setName(c);
            vertexArr[num] = nVertex;
            System.out.println("添加顶点："+c+",所处数组下标为："+num);
            num++;
        }else{
            System.out.println("数组已满！");
        }
    }
    public void addEdge(int from,int to){
        adjMat[from][to] = 1;
        adjMat[to][from] = 1;
    }
    public void showGraph(){
        for(int i=0;i<num;i++){
            for(int j=0;j<num;j++){
                int v = adjMat[i][j];
                System.out.print(v+" ");
            }
            System.out.println();
        }
    }
    public void showVertex(int index){
        System.out.print(vertexArr[index].getName());
    }
    /**
     * 深度优先搜索算法
     *
     */
    public void dfs(){
        vertexArr[0].wasVisited = true;
        showVertex(0);
        sg.push(0);
        while(!sg.isEmpty()){
            int v = getAdjUnvisitedVertex(sg.peek());
            if(v==-1){
                sg.pop();//当当前节点找不到未被访问的临近节点时，将其从栈顶弹出
            }else{
                vertexArr[v].wasVisited = true;
                showVertex(v);
                sg.push(v);
            }
        }
        for(int j=0;j<num;j++){
            vertexArr[j].wasVisited = false;
        }
    }
    /**
     * 此方法根据传入的值查找对应的节点是否有未被访问过的临近节点，如果有，则将找到的第一个符合条件的临近节点的下标返回
     * 否则返回-1
     * @param v
     * @return
     */
    public int getAdjUnvisitedVertex(int v){
        for(int i=0;i<num;i++){
            if(adjMat[v][i]==1&&vertexArr[i].wasVisited==false){
                return i;//找到一个就返回
            }
        }
        return -1;
    }
}

class Vertex{
    private char name;
    private int index;
    public boolean wasVisited;
    public Vertex(){
        wasVisited = false;
    }
    public void setName(char c){
        this.name = c;
    }
    public char getName(){
        return this.name;
    }
    public boolean wasVisited(){
        return this.wasVisited;
    }
}
class StackGraph{
    private int[] st;
    private int top;
    public StackGraph(int size){
        st = new int[size];
        top = -1;
    }
    public void push(int j){
        st[++top] = j;
    }
    public int pop(){
        return st[top--];
    }
    public int peek(){
        return st[top];
    }
    public boolean isEmpty(){
        return top == -1;
    }
}

