import java.util.Scanner;
import java.io.*;
import parcs.*;

public class Matrix implements AM {

    public static void main(String[] args) {
        task curtask = new task();
        curtask.addJarFile("Matrix.jar");
        (new Matrix()).run(new AMInfo(curtask, (channel)null));
        curtask.end();
    }

    public void run(AMInfo info) {
      int n, m;
      Scanner sc;
      try{
        sc = new Scanner(new File(info.curtask.findFile("Matrix.data")));
      }
      catch (IOException e) {e.printStackTrace(); return;}
      n = sc.nextInt();
      m = sc.nextInt();
      int[][] res = new int[n][m];
      for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
        {
        point p = info.createPoint();
        channel c = p.createChannel();
        p.execute("Map");
        c.write(i);
        c.write(j);
  
        System.out.println("Waiting for result...");
        res[i][j] = c.readInt();
        System.out.println("Result found.");
        }
      try{
          PrintWriter out = new PrintWriter(new FileWriter(info.curtask.addPath("Matrix.res")));
          out.println(res);
          out.close();
      } catch (IOException e) {e.printStackTrace(); return;}
    }
}
