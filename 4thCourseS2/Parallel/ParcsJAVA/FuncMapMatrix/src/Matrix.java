import java.util.*;
import java.io.*;
import parcs.*;

public class Matrix implements AM {

    public class Position 
      {
      public int x;
      public int y;
      public Position(int _x, int _y)
        {
        x = _x;
        y = _y;
        }
      }
    
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
      int[][] res = new int[n][m];
      int workers_cnt = 2;
      Queue<point> points = new LinkedList<point>();
      Queue<channel> channels = new LinkedList<channel>();
      Queue<Position> positions = new LinkedList<Position>();
      for (int i = 0; i < n; ++i)
        for (int j = 0; j < m; ++j)
          {
          point p = info.createPoint();
          channel c = p.createChannel();
          p.execute("Map");
          c.write(i);
          c.write(j);
          points.add(p);
          channels.add(c);
          positions.add(new Position(i,j));
          if(points.size() == workers_cnt)
            {
            while(points.size() > 0)
              {
              Position pos = positions.remove();
              channel ch = channels.remove();
              res[pos.x][pos.y] = ch.readInt();
              points.remove();
              }
            }
          }
      try{
          PrintWriter out = new PrintWriter(new FileWriter(info.curtask.addPath("Matrix.res")));
          out.println(res);
          out.close();
      } catch (IOException e) {e.printStackTrace(); return;}
    }
}
