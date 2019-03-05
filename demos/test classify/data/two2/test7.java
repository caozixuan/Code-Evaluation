import java.util.Scanner;
public class test7 {
    public int length=0;
    public String []str=new String[30];
    public int using[]=new int[30];
    public int n;
    public int repeat(String arr,String brr){
        int min=0;
        if(arr.length()<brr.length()){
            min=arr.length();
        }
        else{
            min=brr.length();
        }
        for(int i = 0 ; i < min ; i++ ){
            int flag=1;
            for(int j = 0; j <= i; j++){
                if(arr.charAt(arr.length() -1- i + j) != brr.charAt(j)) {
                    flag = 0;
                }
            }
            if(flag==1) return i+1;
        }
        return 0;
    }
    public void process(String arr,int lengthnow){
        if(length<lengthnow){
            length=lengthnow;
        }
        for(int i = 0; i < n; i++) {
            if(using[i] >= 2) continue;
            int c = repeat(arr, str[i]);
            if(c > 0) {
                using[i]++;
                process(str[i], lengthnow + str[i].length() - c);
                using[i]--;
            }
        }

    }

}