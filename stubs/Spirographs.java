/**
 * 
 */
package cz.tisnik.spirographs;

import java.awt.BorderLayout;
import java.awt.Canvas;
import java.awt.Color;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.SystemColor;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;

class DisplayableImage extends Canvas
{
    private int dr = 0xff/20;
    private int dg = 0xff/20;
    private int db = 0xff/20;

    /**
     * Generated serial version ID.
     */
    private static final long serialVersionUID = 7675486869872952565L;

    private BufferedImage image = null;

    public DisplayableImage(int width, int height)
    {
        this.image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        this.setSize(width, height);
        this.setBackground(Color.BLACK);
    }

    public void clear()
    {
        for (int y = 0; y < image.getHeight(); y++)
        {
            for (int x = 0; x < image.getWidth(); x++)
            {
                putpixel(x, y, 0, 0, 0);
            }
        }
    }

    public void putpixel(int x, int y, int r, int g, int b)
    {
        if (x<0 || y<0 || x>= this.image.getWidth() || y>= this.image.getHeight())
        {
            return;
        }
        this.image.setRGB(x, y, (r<<16) + (g<<8) + (b));
    }

    public void addpixel(int x, int y, int dr, int dg, int db)
    {
        if (x<0 || y<0 || x>= this.image.getWidth() || y>= this.image.getHeight())
        {
            return;
        }
        int pixel = this.image.getRGB(x, y);
        int r = (pixel >> 16) & 0xff;
        int g = (pixel >> 8) & 0xff;
        int b = pixel & 0xff;
        r=addColorItem(r, dr);
        g=addColorItem(g, dg);
        b=addColorItem(b, db);
        this.image.setRGB(x, y, (r<<16) + (g<<8) + (b));
    }

    private int addColorItem(int color, int delta)
    {
        color +=  delta;
        if (color > 0xff)
        {
            color = 0xff;
        }
        return color;
    }

    public void plot(double x, double y)
    {
        addpixel((this.image.getWidth() >> 1) + (int)x, (this.image.getHeight() >> 1) + (int)y, dr, dg, db);
    }

    public void paint(Graphics g)
    {
        g.drawImage(this.image, 0, 0, null);
    }
}

/**
 *
 * @author Pavel Tisnovsky
 */
public class Main
{
    private static final String TITLE = "Fractals - FP benchmark";
    private static final int WIDTH = 512;
    private static final int HEIGHT = 512;
    private static final int BORDER = 1;

    private Frame frame = null;
    private DisplayableImage image = null;

    public Main(String[] args)
    {
        prepareFrame();
        registerEventHandlers();
    }

    private void prepareFrame()
    {
        this.frame = new Frame(TITLE);
        this.frame.setLayout(new BorderLayout(0, 0));
        this.frame.setBackground(SystemColor.control);
        this.frame.add(this.image = new DisplayableImage(WIDTH, HEIGHT), BorderLayout.CENTER);
        this.frame.setSize(WIDTH + BORDER, HEIGHT + BORDER + 20);
        this.frame.setResizable(false);
        this.frame.setVisible(true);
    }

    private void registerEventHandlers()
    {
        this.frame.addWindowListener(new WindowAdapter()
        {
            public void windowClosing(WindowEvent e)
            {
                System.exit(0);
            }
        }
        );
        this.frame.addKeyListener(new KeyListener()
        {
            public void keyPressed(KeyEvent event)
            {
                if (event.getKeyCode() == KeyEvent.VK_ESCAPE)
                {
                    System.exit(0);
                }
            }

            public void keyReleased(KeyEvent event)
            {
            }

            public void keyTyped(KeyEvent event)
            {
            }
        }
        );
    }

    private void run()
    {
        image.clear();
        double R = 100.0;
        double r = 49.0;
        double d = 1.5;
        int steps = 20000;
        int period = 25;
        int lissajousX = 1;//4;
        int lissajousY = 1;//3;

        double endPhi = Math.PI * 2.0 * period;
        for (double phi = 0.0; phi <= endPhi; phi += endPhi / steps / period)
        {
            double x= (R + r) * Math.cos(phi*lissajousX) + r * d * Math.cos(phi*(R+r)/r);
            double y= (R + r) * Math.sin(phi*lissajousY) - r * d * Math.sin(phi*(R+r)/r);
            image.plot(x, y);
            //r*=0.99999;
        }
        image.repaint();
    }

    /**
     * @param args
     */
    public static void main(String[] args)
    {
        new Main(args).run();
    }

}
