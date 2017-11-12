function draw_des_prediction()
    Y = [0.01675 0.98325; 0.20825 0.79175];
    X = {'High Influential', 'Less Influential'};
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
    legend('w/o Bio', 'w/ Bio', 'Location', 'EastOutside');
    set(legend, 'FontSize', 20);
    title('');
    grid off;
    print('./results/prediction/attributes/des_prediction.eps', '-depsc')
end