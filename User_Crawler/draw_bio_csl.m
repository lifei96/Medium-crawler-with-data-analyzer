function draw_bio_csl()
    Y = [0.0489445253358, 0.784081000616, 0.0338420034163, 0.133132470632; 0.159476385506, 0.194338455794, 0.589157986155, 0.0570271725451];
    X = {'w/ Bio', 'w/o Bio'};
    bar(Y, 0.8, 'stacked');
    colormap(copper);
    xlim([0.5 2.5]); 
    ylim([0 1]);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'xticklabel', X);
    set(gca, 'FontSize', 12);
    ax = gca;
    ax.XAxis.FontSize = 18;
    xlabel(' ','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    legend('Neither', 'TW only', 'FB only', 'Both', 'Location', 'EastOutside');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/csl/bio_csl.eps', '-depsc');
end