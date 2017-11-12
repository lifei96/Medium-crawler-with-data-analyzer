function draw_CC()
    dataset = csvread('./data/graph/CC.csv', 1, 1);
    a = dataset(:,1);
    b = a(a<=1 & a>=0);
    disp(mean(b));
    h = cdfplot(b);
    xlim([0 1]);
    set(h, 'color', 'k', 'LineStyle', '-', 'LineWidth', 2);
    set(gca, 'yticklabel', cellstr(num2str(get(gca,'ytick')'*100)));
    set(gca, 'FontSize', 12);
    xlabel('Clustering Coefficient','FontSize',20);
    ylabel('Percentage(%)','FontSize',20);
    title('');
    grid off;
    print('./results/graph/CDF_CC.eps', '-depsc');
end