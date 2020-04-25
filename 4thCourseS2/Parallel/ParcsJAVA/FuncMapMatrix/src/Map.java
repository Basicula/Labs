import parcs.*;

public class Map implements AM{
    public void run(AMInfo info){
        int x,y,r;
        x = info.parent.readInt();
        System.out.println(x);
        //y = info.parent.readInt();
        //System.out.print('+');
        //System.out.print(y);
        //r = x+y;
        info.parent.write(x);
    }
}
