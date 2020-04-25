import java.util.*;
import java.io.*;
import parcs.*;

public class Matrix implements AM {
    private static int _workers_cnt;
    public static void main(String[] args) {
        for (int workers_cnt : new int[]{1, 2, 4, 8})
          {
          _workers_cnt = workers_cnt;
          long startTime = System.nanoTime();
          task curtask = new task();
          curtask.addJarFile("Matrix.jar");
          (new Matrix()).run(new AMInfo(curtask, (channel)null));
          curtask.end();
          long endTime = System.nanoTime();
          long duration = (endTime - startTime);
          System.out.println("Task with " + workers_cnt + " workers takes " + duration / 1000000 + "milliseconds");
          }
    }

    public void run(AMInfo info) {
      int n, m;
      Scanner sc;
      try{
        sc = new Scanner(new File(info.curtask.findFile("LargeExample.data")));
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
      point[] points = new point[_workers_cnt];
      channel[] channels = new channel[_workers_cnt];
      for (int i = 0; i < _workers_cnt; ++i)
        {
        points[i] = info.createPoint();
        channels[i] = points[i].createChannel();
        points[i].execute("Map");
        channels[i].write(n / _workers_cnt);
        channels[i].write(m);
        }
      System.out.println("Channels have started");
      for (int i = 0; i < n / _workers_cnt; ++i)
        for (int j = 0; j < m; ++j)
          {
          for (int k = 0; k < _workers_cnt; ++k)
            {
            point p = points[k];
            channel c = channels[k];
            c.write(matrix[i + k * n / _workers_cnt][j]);
            }
          }
      System.out.println("Info have filled\nWaiting for results");
      for (int i = 0; i < n / _workers_cnt; ++i)
        for (int j = 0; j < m; ++j)
          {
          for (int k = 0; k < _workers_cnt; ++k)
            {
            point p = points[k];
            channel c = channels[k];
            res[i + k * n / _workers_cnt][j] = c.readInt();
            }
          }
      try{
          PrintWriter out = new PrintWriter(new FileWriter(info.curtask.addPath("LargeExample"+_workers_cnt+".res")));
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
