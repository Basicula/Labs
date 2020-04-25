import parcs.*;

public class Map implements AM{
    static int gcd(int a, int b) 
      { 
          if (a == 0) 
              return b; 
          return gcd(b % a, a); 
      } 
    
    static int phi(int n) 
      { 
        int result = 1; 
        for (int i = 2; i < n; i++) 
            if (gcd(i, n) == 1) 
                result++; 
        return result; 
      } 
  
    public void run(AMInfo info){
        int n,m;
        n = info.parent.readInt();
        m = info.parent.readInt();
        System.out.println("Size: "+n+"x"+m);
        int[][] temp = new int[n][m];
        for (int i = 0; i < n; ++i)
          for (int j = 0; j < m; ++j)
            temp[i][j] = info.parent.readInt();
        System.out.println("Temp matrix have read");
        for (int i = 0; i < n; ++i)
          for (int j = 0; j < m; ++j)
            {
            int r = phi(temp[i][j]);
            info.parent.write(r);
            }
    }
}
