import java.util.*;
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
      System.out.println("Size: " + n + "x" + m);
      
      int[][] matrix = new int[n][m];
      for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
          matrix[i][j] = sc.nextInt();
      System.out.println("Matrix has read");
      
      int[][] res = new int[n][m];
      int workers_cnt = 2;
      point[] points = new point[workers_cnt];
      channel[] channels = new channel[workers_cnt];
      for (int i = 0; i < workers_cnt; ++i)
        {
        points[i] = info.createPoint();
        points[i].execute("Map");
        channels[i] = points[i].createChannel();
        channels[i].write(n / workers_cnt);
        channels[i].write(m);
        }
      System.out.println("Channels have started");
      for (int i = 0; i < n / workers_cnt; ++i)
        for (int j = 0; j < m; ++j)
          {
          for (int k = 0; k < workers_cnt; ++k)
            {
            point p = points[k];
            channel c = channels[k];
            c.write(matrix[i + k * n / workers_cnt][j]);
            }
          }
      System.out.println("Info have filled\nWaiting for results");
      for (int i = 0; i < n / workers_cnt; ++i)
        for (int j = 0; j < m; ++j)
          {
          for (int k = 0; k < workers_cnt; ++k)
            {
            point p = points[k];
            channel c = channels[k];
            res[i + k * n / workers_cnt][j] = c.readInt();
            }
          }
      try{
          PrintWriter out = new PrintWriter(new FileWriter(info.curtask.addPath("Matrix.res")));
          for (int i = 0; i < n; ++i)
            {
            for (int j = 0; j < m; ++j)
              out.print(res[i][j] + " ");
            out.println();
            }
          out.close();
      } catch (IOException e) {e.printStackTrace(); return;}
    }
}
